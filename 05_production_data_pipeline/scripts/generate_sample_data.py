"""
[MLOps Full-Stack 05강] generate_sample_data.py
- 실습용 이커머스 고객 데이터셋 자동 생성기
- 결측치(Null), 음수 값, 비정상 이상치(Outlier)가 포함된 현실적인 Raw Data를 생성합니다.
"""

import sys
import random
import csv
from pathlib import Path

# Windows 콘솔 인코딩 대응
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def generate_raw_ecommerce_csv(output_path: Path, num_records: int = 1000):
    """결측치와 이상치가 주입된 원본 CSV 데이터셋 생성"""
    random.seed(42)

    tiers = ["Bronze", "Silver", "Gold", "VIP", None]
    rows = [["user_id", "age", "purchase_amount", "membership_tier", "days_since_last_login", "churn"]]

    for i in range(1, num_records + 1):
        user_id = f"USR-{i:05d}"

        # 1. Age (나이): 기본 20~65세, 가끔 결측치(None) 또는 이상치(-5세, 180세) 주입
        rand_val = random.random()
        if rand_val < 0.05:
            age = ""  # 결측치
        elif rand_val < 0.08:
            age = random.choice([-5, 180, 250])  # 비정상 이상치
        else:
            age = random.randint(20, 65)

        # 2. Purchase Amount (구매 금액): 기본 10.0 ~ 500.0, 가끔 결측치 또는 이상치(-100, 99999)
        rand_val = random.random()
        if rand_val < 0.06:
            amount = ""  # 결측치
        elif rand_val < 0.09:
            amount = round(random.choice([-100.0, 99999.0]), 2)  # 이상치
        else:
            amount = round(random.uniform(10.0, 500.0), 2)

        # 3. Membership Tier (멤버십 등급): 가끔 결측치
        tier = random.choice(tiers) or ""

        # 4. Days Since Last Login: 0~365
        days_login = random.randint(0, 365)

        # 5. Churn (이탈 여부): 0 또는 1
        churn = 1 if (days_login > 180 or (isinstance(amount, float) and amount < 50.0)) else 0

        rows.append([user_id, age, amount, tier, days_login, churn])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"[INFO] 원본 샘플 데이터셋 생성 완료: {output_path} (총 {num_records}건)")


def main():
    data_dir = Path(__file__).resolve().parent.parent / "data"
    csv_file = data_dir / "raw_ecommerce_data.csv"
    generate_raw_ecommerce_csv(csv_file, num_records=1000)


if __name__ == "__main__":
    main()
