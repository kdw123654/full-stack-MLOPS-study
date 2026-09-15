"""
[MLOps Full-Stack 02강] 02_pydantic_validation.py
- Pydantic v2 기반 MLOps 데이터 유효성 검증(Validation) 완벽 실습
- 모델 서빙 시 비정상 입력(Garbage In) 원천 차단
- field_validator 및 model_validator를 활용한 도메인 룰 검증
"""

import sys
import json
from datetime import datetime
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, field_validator, model_validator, ValidationError

# Windows cp949 인코딩 콘솔 대응
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    console = Console(legacy_windows=False)
    HAS_RICH = True
except Exception:
    console = None
    HAS_RICH = False


# =====================================================================
# 1. MLOps 입력 데이터 스키마 정의 (고객 이탈 예측 모델 예시)
# =====================================================================
class CustomerFeature(BaseModel):
    """
    단일 고객의 머신러닝 Feature 스키마.
    Pydantic이 타입을 자동 변환(Coercion)하고 범위를 강제합니다.
    """
    customer_id: str = Field(..., description="고객 고유 식별자 (예: CUST-1001)")
    age: int = Field(..., ge=18, le=100, description="고객 나이 (18세 이상 100세 이하만 서비스 이용 가능)")
    monthly_charges: float = Field(..., ge=0.0, description="월 이용 요금 ($0 이상)")
    total_charges: float = Field(..., ge=0.0, description="총 누적 요금 ($0 이상)")
    tenure_months: int = Field(..., ge=0, description="가입 개월 수 (0개월 이상)")
    contract_type: Literal["month-to-month", "one-year", "two-year"] = Field(
        ..., description="계약 유형 (허용된 3가지 옵션만 가능)"
    )
    is_senior: Optional[bool] = Field(default=False, description="고령자 여부")

    # [필드 검증 1]: 고객 ID 포맷 검증
    @field_validator("customer_id")
    @classmethod
    def validate_customer_id(cls, v: str) -> str:
        if not v.startswith("CUST-"):
            raise ValueError(f"고객 ID는 반드시 'CUST-'로 시작해야 합니다. 입력값: '{v}'")
        return v

    # [모델 전체 검증 2]: 필드 간 논리적 모순 검증 (Cross-field Validation)
    @model_validator(mode="after")
    def validate_charges_consistency(self) -> "CustomerFeature":
        # 가입 기간이 0개월인데 총 요금이 발생한 이상치 검출
        if self.tenure_months == 0 and self.total_charges > 0:
            raise ValueError(
                f"가입 개월 수가 0개월인데 총 누적 요금(${self.total_charges})이 존재할 수 없습니다."
            )
        # 총 요금이 (월 요금 * 가입 개월 수)에 비해 비정상적으로 터무니없는 경우 방지 (예: 마이너스 오차 등)
        return self


# =====================================================================
# 2. 배치 추론 요청 및 응답 스키마
# =====================================================================
class BatchInferenceRequest(BaseModel):
    """FastAPI 및 서빙 서버로 전달되는 배치 예측 요청 규격"""
    request_id: str = Field(..., description="요청 추적용 UUID")
    model_version: str = Field(default="v1.0.0", description="요청 모델 버전")
    features: List[CustomerFeature] = Field(..., min_length=1, description="1건 이상의 고객 피처 리스트")


class SinglePredictionResult(BaseModel):
    """단일 예측 결과"""
    customer_id: str
    churn_probability: float = Field(..., ge=0.0, le=1.0)
    prediction: Literal["Churn", "Stay"]
    predicted_at: datetime = Field(default_factory=datetime.utcnow)


# =====================================================================
# 3. 실무 테스트: 정상 데이터 vs 비정상 데이터 유효성 검사 시뮬레이션
# =====================================================================
def run_validation_simulation():
    # 1. 정상 데이터
    valid_payload = {
        "request_id": "REQ-2026-001",
        "model_version": "v1.2.0",
        "features": [
            {
                "customer_id": "CUST-1001",
                "age": 29,
                "monthly_charges": 65.5,
                "total_charges": 786.0,
                "tenure_months": 12,
                "contract_type": "one-year",
                "is_senior": False
            },
            {
                "customer_id": "CUST-1002",
                "age": 67,
                "monthly_charges": 99.0,
                "total_charges": 0.0,
                "tenure_months": 0,
                "contract_type": "month-to-month",
                "is_senior": True
            }
        ]
    }

    # 2. 비정상 데이터 (이상치 및 타입 오류 포함)
    invalid_payloads = [
        {
            "desc": "❌ 나이 제한 위반 (18세 미만)",
            "data": {
                "customer_id": "CUST-9999",
                "age": 15, # 에러: ge=18 위반
                "monthly_charges": 30.0,
                "total_charges": 30.0,
                "tenure_months": 1,
                "contract_type": "month-to-month"
            }
        },
        {
            "desc": "❌ 고객 ID 규칙 위반 (CUST- 접두사 누락)",
            "data": {
                "customer_id": "USER-5555", # 에러: custom validator 위반
                "age": 40,
                "monthly_charges": 50.0,
                "total_charges": 500.0,
                "tenure_months": 10,
                "contract_type": "month-to-month"
            }
        },
        {
            "desc": "❌ 논리적 모순 (0개월 차인데 총 요금 500달러 발생)",
            "data": {
                "customer_id": "CUST-8888",
                "age": 35,
                "monthly_charges": 50.0,
                "total_charges": 500.0, # 에러: 0개월인데 총요금 > 0
                "tenure_months": 0,
                "contract_type": "month-to-month"
            }
        },
        {
            "desc": "❌ 허용되지 않은 계약 유형 (오타)",
            "data": {
                "customer_id": "CUST-7777",
                "age": 22,
                "monthly_charges": 45.0,
                "total_charges": 450.0,
                "tenure_months": 10,
                "contract_type": "lifetime" # 에러: Literal 범주 외
            }
        }
    ]

    # 터미널 출력
    if HAS_RICH and console:
        console.print(Panel.fit("[bold cyan]🛡️ MLOps 02강: Pydantic v2 데이터 검증 파이프라인 시연[/bold cyan]"))
        
        # 정상 검증 시연
        try:
            req = BatchInferenceRequest(**valid_payload)
            table_ok = Table(title="✅ 1. 정상 배치 데이터 검증 통과 (FastAPI 모델 서빙 연동)", header_style="bold green")
            table_ok.add_column("고객 ID")
            table_ok.add_column("나이")
            table_ok.add_column("월 요금")
            table_ok.add_column("계약 형태")
            table_ok.add_column("검증 상태", style="bold green")
            for feat in req.features:
                table_ok.add_row(feat.customer_id, str(feat.age), f"${feat.monthly_charges}", feat.contract_type, "PASS (정상)")
            console.print(table_ok)
        except ValidationError as e:
            console.print(f"[red]예상치 못한 검증 실패: {e}[/red]")

        # 비정상 데이터 차단 시연
        table_err = Table(title="🚫 2. 비정상 이상치 데이터 사전 차단 (Garbage In 차단)", header_style="bold red")
        table_err.add_column("테스트 시나리오", style="dim", width=30)
        table_err.add_column("차단 이유 (Pydantic 에러 메시지)", style="bold red")

        for item in invalid_payloads:
            try:
                CustomerFeature(**item["data"])
            except ValidationError as err:
                err_msg = err.errors()[0]["msg"]
                table_err.add_row(item["desc"], err_msg)
        console.print(table_err)

    else:
        print("=== [02강] Pydantic v2 데이터 검증 시연 ===")
        req = BatchInferenceRequest(**valid_payload)
        print(f"정상 데이터 검증 성공: {len(req.features)}건 파싱 완료")
        for item in invalid_payloads:
            try:
                CustomerFeature(**item["data"])
            except ValidationError as err:
                print(f"{item['desc']} -> 차단 완료: {err.errors()[0]['msg']}")


if __name__ == "__main__":
    run_validation_simulation()
