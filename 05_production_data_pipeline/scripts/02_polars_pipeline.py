"""
[MLOps Full-Stack 05강] 02_polars_pipeline.py
- Rust 기반의 초고속 차세대 데이터 프레임워크 Polars 실무 파이프라인
- LazyFrame을 활용한 지연 평가(Lazy Evaluation)와 Parquet 초고속 저장
"""

import sys
import time
from pathlib import Path
import polars as pl

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


def run_polars_lazy_pipeline(raw_csv_path: Path, output_parquet_path: Path):
    """Polars의 scan_csv()와 LazyFrame을 이용한 고속 파이프라인"""
    start_time = time.time()

    # 1. scan_csv: 데이터를 즉시 메모리에 올리지 않고 쿼리 플랜만 수립 (Lazy)
    q = pl.scan_csv(raw_csv_path)

    # 2. 이상치 필터링 & 결측치 대체 표현식(Expressions) 체이닝
    # Polars에서는 pl.when().then().otherwise() 를 사용하여 조건별 치환을 초고속 멀티스레드로 처리합니다.
    q_transformed = q.with_columns([
        # Age: 18~100 사이가 아니면 null, 이후 중앙값(42)으로 대체
        pl.when((pl.col("age") >= 18) & (pl.col("age") <= 100))
        .then(pl.col("age"))
        .otherwise(None)
        .fill_null(pl.col("age").median())
        .alias("age_clean"),

        # Purchase Amount: 0~5000 사이가 아니면 null, 이후 평균값으로 대체
        pl.when((pl.col("purchase_amount") >= 0) & (pl.col("purchase_amount") <= 5000))
        .then(pl.col("purchase_amount"))
        .otherwise(None)
        .fill_null(pl.col("purchase_amount").mean())
        .alias("purchase_amount_clean"),

        # Membership Tier: null이면 "Bronze"로 채우기
        pl.col("membership_tier").fill_null("Bronze").alias("tier_clean"),
    ])

    # 3. 파생 피처 엔지니어링: 고가치 고객 플래그 생성
    q_final = q_transformed.with_columns([
        (pl.col("purchase_amount_clean") >= 250.0).cast(pl.Int32).alias("is_high_value_customer")
    ])

    # 4. collect(): 실제 연산 수행 (지연되었던 모든 최적화 쿼리가 C++/Rust 코어에서 병렬 실행)
    df_clean = q_final.collect()

    # 5. Parquet 초고속 압축 포맷으로 저장 (MLOps 표준)
    output_parquet_path.parent.mkdir(parents=True, exist_ok=True)
    df_clean.write_parquet(output_parquet_path)

    elapsed = time.time() - start_time
    return df_clean, elapsed


def main():
    base_dir = Path(__file__).resolve().parent.parent
    raw_csv = base_dir / "data" / "raw_ecommerce_data.csv"
    output_parquet = base_dir / "data" / "processed_polars_data.parquet"

    df_result, elapsed_sec = run_polars_lazy_pipeline(raw_csv, output_parquet)

    if HAS_RICH and console:
        console.print(Panel.fit("[bold cyan]⚡ 05강: Polars 차세대 초고속 Lazy 파이프라인 완료[/bold cyan]"))

        table = Table(title="🚀 Polars 파이프라인 처리 성과", header_style="bold yellow")
        table.add_column("항목")
        table.add_column("결과 값", style="bold green")
        table.add_row("처리된 데이터 크기", f"{df_result.shape[0]:,} 행 × {df_result.shape[1]} 열")
        table.add_row("총 소요 시간", f"{elapsed_sec:.4f} 초 (초고속 병렬 처리)")
        table.add_row("저장 포맷", "Apache Parquet (컬럼 기반 압축 포맷)")
        table.add_row("출력 파일 경로", str(output_parquet.name))
        console.print(table)

        # Polars 데이터프레임 미리보기
        table_view = Table(title="👀 Polars 결과 데이터셋 (Top 5)", header_style="bold magenta")
        cols = ["user_id", "age_clean", "purchase_amount_clean", "tier_clean", "is_high_value_customer"]
        for c in cols:
            table_view.add_column(c)
        for row in df_result.select(cols).head(5).iter_rows():
            table_view.add_row(*[f"{val:.2f}" if isinstance(val, float) else str(val) for val in row])
        console.print(table_view)
    else:
        print(f"Polars 실행 완료: {df_result.shape}, 소요시간: {elapsed_sec:.4f}s")
        print(df_result.head())


if __name__ == "__main__":
    main()
