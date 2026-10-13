# 📝 [제5강 과제] 금융 거래 데이터 정제 및 이상치 파이프라인 구현

축하합니다! 5강에서는 프로덕션 레벨의 **Pandas 파이프라인, Rust 기반 Polars의 Lazy 연산, 그리고 데이터 품질 검증**을 배웠습니다.  
이번 과제는 배운 내용을 응용하여 **금융 신용카드 거래 데이터(Fraud Detection)를 정제하는 실무 파이프라인 함수**를 완성하는 실습 미션입니다.

---

## 🎯 과제 목표
금융 거래 원본 데이터(`raw_transactions`)에 포함된 결측치(None)와 이상치를 정제하고, 사기 탐지 모델 학습을 위한 파생 피처를 생성하는 `clean_financial_transactions(df)` 함수를 완성하세요.

### 📋 세부 요구 조건
1. **결측치(Null) 보정**:
   - `amount` (거래 금액): 결측치는 전체 거래 금액의 **중앙값(Median)**으로 대체
   - `device_type` (기기 유형): 결측치는 `"UNKNOWN"` 문자열로 대체
2. **이상치(Outlier) 처리**:
   - `user_age` (고객 나이): 18세 미만이거나 100세 초과인 비정상 값은 전체 정상 고객의 **평균 나이(반올림)**로 치환
3. **파생 피처 생성**:
   - `is_large_transaction`: `amount >= 1000.0` 이면 `1`, 아니면 `0` (정수형)
4. **품질 검증**:
   - 최종 데이터프레임의 전체 결측치(Null) 합계가 정확히 `0`개여야 함.

---

## 💻 실습 코드 템플릿 (`assignments/solution_05.py`에 작성)

```python
import pandas as pd
import numpy as np

# ===============================================================
# 테스트용 원본 금융 거래 데이터
# ===============================================================
raw_data = {
    "tx_id": ["TX-001", "TX-002", "TX-003", "TX-004", "TX-005", "TX-006"],
    "amount": [150.0, None, 2500.0, 45.0, 9999.0, None],
    "user_age": [28, -5, 45, 150, 34, 62],  # -5세와 150세 이상치 포함
    "device_type": ["iOS", "Android", None, "Web", "iOS", None]
}


def clean_financial_transactions(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # 1. user_age 이상치 처리 (-5, 150 등 비정상치를 NaN 치환 후 정상 평균으로 보정)
    valid_age_mean = round(df.loc[(df["user_age"] >= 18) & (df["user_age"] <= 100), "user_age"].mean())
    df.loc[(df["user_age"] < 18) | (df["user_age"] > 100), "user_age"] = valid_age_mean

    # 2. amount 결측치 중앙값(Median) 보정
    amount_median = df["amount"].median()
    df["amount"] = df["amount"].fillna(amount_median)

    # 3. device_type 결측치 'UNKNOWN' 보정
    df["device_type"] = df["device_type"].fillna("UNKNOWN")

    # 4. is_large_transaction 파생 피처 생성 ($1000 이상 여부)
    df["is_large_transaction"] = (df["amount"] >= 1000.0).astype(int)

    return df


if __name__ == "__main__":
    df_raw = pd.DataFrame(raw_data)
    df_clean = clean_financial_transactions(df_raw)

    print("=" * 60)
    print("📊 [제5강 과제] 금융 거래 정제 파이프라인 결과")
    print("=" * 60)
    print(df_clean)
    print("-" * 60)

    total_nulls = df_clean.isnull().sum().sum()
    print(f"잔여 결측치 수: {total_nulls}개 ({'✅ 완벽 정제' if total_nulls == 0 else '❌ 실패'})")
    assert total_nulls == 0, "결측치가 남아 있습니다!"
    print("🎉 5강 과제 검증 통과 완료!")
```

---

## 🚀 과제 실행 및 Git 커밋
코드를 완성하고 실행하여 검증을 통과하면 GitHub에 커밋하고 푸시합니다:

```powershell
git status
git add .
git commit -m "feat: complete lesson 05 production data pipeline and homework"
git push origin main
```
