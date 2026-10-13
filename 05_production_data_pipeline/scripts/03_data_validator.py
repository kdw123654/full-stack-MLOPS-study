"""
[MLOps Full-Stack 05강] 03_data_validator.py
- 프로덕션 데이터 계약(Data Contract) 및 품질 검증기 (Data Quality Validator)
- 전처리 파이프라인 전/후에 비정상 데이터 유입을 감지하여 학습/서빙 실패를 방지합니다.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any
import pandas as pd

# Windows 콘솔 인코딩 대응
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    console = Console(legacy_windows=False)
    HAS_RICH = True
except Exception:
    console = None
    HAS_RICH = False


class DataQualityValidator:
    """MLOps 데이터 품질 및 스키마 검증기"""

    def __init__(self, expected_columns: List[str], max_null_ratio: float = 0.10):
        self.expected_columns = expected_columns
        self.max_null_ratio = max_null_ratio
        self.validation_results = []

    def validate(self, df: pd.DataFrame) -> bool:
        is_passed = True

        # 1. 스키마 컬럼 검증
        missing_cols = set(self.expected_columns) - set(df.columns)
        if missing_cols:
            self.validation_results.append({
                "rule": "1. 필수 스키마 컬럼 존재 여부",
                "status": "FAIL",
                "message": f"누락된 컬럼 감지: {list(missing_cols)}"
            })
            is_passed = False
        else:
            self.validation_results.append({
                "rule": "1. 필수 스키마 컬럼 존재 여부",
                "status": "PASS",
                "message": f"모든 필수 컬럼({len(self.expected_columns)}개) 확인 완료"
            })

        # 2. 결측치(Null) 비율 검증
        null_ratios = df.isnull().mean()
        high_null_cols = null_ratios[null_ratios > self.max_null_ratio]
        if not high_null_cols.empty:
            self.validation_results.append({
                "rule": f"2. 결측치 비율 (최대 {int(self.max_null_ratio*100)}% 이하)",
                "status": "FAIL",
                "message": f"허용 초과 컬럼: {high_null_cols.to_dict()}"
            })
            is_passed = False
        else:
            self.validation_results.append({
                "rule": f"2. 결측치 비율 (최대 {int(self.max_null_ratio*100)}% 이하)",
                "status": "PASS",
                "message": f"모든 컬럼의 결측치 비율이 기준치({int(self.max_null_ratio*100)}%) 미만임"
            })

        # 3. 값의 유효 범위 검증 (Cleaned Data 기준: age >= 0, purchase_amount >= 0)
        invalid_conditions = []
        if "age" in df.columns and (df["age"] < 0).any():
            invalid_conditions.append("음수 나이 발견")
        if "purchase_amount" in df.columns and (df["purchase_amount"] < 0).any():
            invalid_conditions.append("음수 구매 금액 발견")

        if invalid_conditions:
            self.validation_results.append({
                "rule": "3. 수치형 피처 허용 범위 (음수값 금지)",
                "status": "FAIL",
                "message": f"이상치 발견: {invalid_conditions}"
            })
            is_passed = False
        else:
            self.validation_results.append({
                "rule": "3. 수치형 피처 허용 범위 (음수값 금지)",
                "status": "PASS",
                "message": "음수 비정상 값 없음 (정상 범위)"
            })

        return is_passed


def main():
    base_dir = Path(__file__).resolve().parent.parent
    raw_csv = base_dir / "data" / "raw_ecommerce_data.csv"
    processed_csv = base_dir / "data" / "processed_pandas_data.csv"

    validator = DataQualityValidator(
        expected_columns=["user_id", "age", "purchase_amount", "days_since_last_login", "churn"],
        max_null_ratio=0.08
    )

    # 1. 정제된 데이터 검증 시연
    df_clean = pd.read_csv(processed_csv) if processed_csv.exists() else None
    if df_clean is not None:
        clean_passed = validator.validate(df_clean)

        if HAS_RICH and console:
            console.print(Panel.fit("[bold blue]🛡️ 05강: 정제 데이터 품질 검증 결과 (Data Quality Report)[/bold blue]"))
            table = Table(title="데이터 검증 룰 요약", header_style="bold cyan")
            table.add_column("검증 규칙", style="dim", width=35)
            table.add_column("결과", justify="center", width=10)
            table.add_column("상세 메시지")

            for res in validator.validation_results:
                style = "bold green" if res["status"] == "PASS" else "bold red"
                table.add_row(res["rule"], f"[{style}]{res['status']}[/{style}]", res["message"])
            console.print(table)
        else:
            print(f"검증 통과 여부: {clean_passed}")
            for r in validator.validation_results:
                print(r)


if __name__ == "__main__":
    main()
