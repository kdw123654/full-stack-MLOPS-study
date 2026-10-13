"""
[MLOps Full-Stack 05강] 01_pandas_pipeline.py
- Pandas 기반의 재현 가능한(Reproducible) 프로덕션 데이터 전처리 파이프라인
- 결측치(Imputation), 이상치 필터링, 범주형 인코딩, 정규화의 실무 모듈화
"""

import sys
from pathlib import Path
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


class PandasEcommercePipeline:
    """모듈화된 이커머스 고객 데이터 전처리 파이프라인"""

    def __init__(self, raw_path: Path, output_path: Path):
        self.raw_path = raw_path
        self.output_path = output_path
        self.stats = {}

    def load_data(self) -> pd.DataFrame:
        """1단계: 원본 데이터 로드"""
        if not self.raw_path.exists():
            raise FileNotFoundError(f"원본 데이터를 찾을 수 없습니다: {self.raw_path}")
        df = pd.read_csv(self.raw_path)
        self.stats["initial_rows"] = len(df)
        self.stats["initial_nulls"] = df.isnull().sum().to_dict()
        return df

    def clean_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """2단계: 비정상 이상치(Outlier)를 NaN으로 변환하여 정제 준비"""
        df = df.copy()

        # Age: 18세 미만 또는 100세 초과 비정상치는 NaN으로 치환
        df.loc[(df["age"] < 18) | (df["age"] > 100), "age"] = None

        # Purchase Amount: 0원 미만 또는 $5000 초과 비정상치는 NaN으로 치환
        df.loc[(df["purchase_amount"] < 0) | (df["purchase_amount"] > 5000), "purchase_amount"] = None

        return df

    def impute_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """3단계: 결측치 대체 (Imputation)"""
        df = df.copy()

        # Age: 중앙값(Median)으로 보정
        median_age = df["age"].median()
        df["age"] = df["age"].fillna(median_age)

        # Purchase Amount: 평균값(Mean)으로 보정
        mean_amount = round(df["purchase_amount"].mean(), 2)
        df["purchase_amount"] = df["purchase_amount"].fillna(mean_amount)

        # Membership Tier: 결측치는 기본 등급인 "Bronze"로 보정
        df["membership_tier"] = df["membership_tier"].fillna("Bronze")

        self.stats["impute_age_median"] = median_age
        self.stats["impute_amount_mean"] = mean_amount
        return df

    def encode_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """4단계: 범주형 변수(Membership Tier) 원핫 인코딩"""
        df = pd.get_dummies(df, columns=["membership_tier"], prefix="tier", drop_first=False, dtype=int)
        return df

    def run(self) -> pd.DataFrame:
        """파이프라인 전체 실행"""
        df_raw = self.load_data()
        df_cleaned = self.clean_outliers(df_raw)
        df_imputed = self.impute_missing_values(df_cleaned)
        df_final = self.encode_features(df_imputed)

        # 정제 데이터 저장
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        df_final.to_csv(self.output_path, index=False)
        self.stats["final_rows"] = len(df_final)
        self.stats["final_nulls"] = df_final.isnull().sum().sum()

        return df_final


def main():
    base_dir = Path(__file__).resolve().parent.parent
    raw_csv = base_dir / "data" / "raw_ecommerce_data.csv"
    processed_csv = base_dir / "data" / "processed_pandas_data.csv"

    # 만약 원본 데이터가 없으면 자동 생성기 호출
    if not raw_csv.exists():
        from generate_sample_data import generate_raw_ecommerce_csv
        generate_raw_ecommerce_csv(raw_csv, num_records=1000)

    pipeline = PandasEcommercePipeline(raw_csv, processed_csv)
    df_result = pipeline.run()

    if HAS_RICH and console:
        console.print(Panel.fit("[bold green]🐼 05강: Pandas 프로덕션 전처리 파이프라인 완료[/bold green]"))

        table_stats = Table(title="📊 데이터 정제 전/후 통계 비교", header_style="bold cyan")
        table_stats.add_column("항목", style="dim")
        table_stats.add_column("정제 전", style="bold yellow")
        table_stats.add_column("정제 후 (Clean)", style="bold green")

        table_stats.add_row("전체 행(Row) 수", f"{pipeline.stats['initial_rows']:,} 건", f"{pipeline.stats['final_rows']:,} 건")
        table_stats.add_row("잔여 결측치(Null) 총합", f"{sum(pipeline.stats['initial_nulls'].values()):,} 개", f"{pipeline.stats['final_nulls']} 개 (완벽 정제)")
        table_stats.add_row("나이(Age) 결측치 대체값", "-", f"{pipeline.stats['impute_age_median']:.1f} 세 (중앙값)")
        table_stats.add_row("구매금액 결측치 대체값", "-", f"${pipeline.stats['impute_amount_mean']:.2f} (평균값)")
        console.print(table_stats)

        # 상위 5행 출력
        table_preview = Table(title="👀 정제된 데이터셋 상위 5건 미리보기", header_style="bold magenta")
        for col in df_result.columns[:7]:
            table_preview.add_column(col)
        for _, row in df_result.head(5).iterrows():
            table_preview.add_row(*[str(row[c]) for c in df_result.columns[:7]])
        console.print(table_preview)
    else:
        print("=== Pandas 파이프라인 완료 ===")
        print(f"최종 데이터 크기: {df_result.shape}, 결측치 수: {df_result.isnull().sum().sum()}")
        print(df_result.head())


if __name__ == "__main__":
    main()
