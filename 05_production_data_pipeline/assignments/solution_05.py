"""
[MLOps Full-Stack 05강 과제 정답] solution_05.py
- 금융 거래 데이터 정제 및 이상치 처리 파이프라인 완성본
"""

import sys
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

    # 1. user_age 이상치 처리 (-5, 150 등 비정상치를 제외한 정상 고객의 평균 나이로 치환)
    valid_mask = (df["user_age"] >= 18) & (df["user_age"] <= 100)
    valid_age_mean = round(df.loc[valid_mask, "user_age"].mean())
    df.loc[~valid_mask, "user_age"] = valid_age_mean

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

    print("=" * 65)
    print("📊 [제5강 과제 정답] 금융 거래 데이터 정제 파이프라인 결과")
    print("=" * 65)
    print(df_clean.to_string(index=False))
    print("-" * 65)

    total_nulls = df_clean.isnull().sum().sum()
    print(f"잔여 결측치 수: {total_nulls}개 ({'✅ 완벽 정제' if total_nulls == 0 else '❌ 실패'})")
    assert total_nulls == 0, "결측치가 남아 있습니다!"
    print("🎉 5강 과제 모든 검증 테스트 통과 완료!")
