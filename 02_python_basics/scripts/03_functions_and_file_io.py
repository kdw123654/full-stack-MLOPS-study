"""
[MLOps Full-Stack 02강] 03_functions_and_file_io.py
- 함수의 정의와 매개변수 (*args, **kwargs)
- 에러를 우아하게 다루는 예외 처리 (try - except - finally)
- 데이터 저장과 불러오기의 기본: 파일 입출력 (with open) 및 CSV 다루기
"""

import sys
import csv
from pathlib import Path

# Windows 콘솔 인코딩 대응
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
# 1. 함수 정의와 매개변수 (*args, **kwargs)
# =====================================================================
def calculate_model_score(base_acc: float, bonus: float = 0.0, **metadata) -> dict:
    """
    기본 점수와 보너스, 그리고 임의의 메타데이터 키워드 인자(**kwargs)를 받아
    최종 모델 결과 딕셔너리를 생성하는 함수.
    """
    total_score = min(1.0, base_acc + bonus)
    return {
        "final_score": round(total_score, 4),
        "details": metadata
    }


def safe_divide(numerator: float, denominator: float) -> float:
    """
    2. 예외 처리 (try - except)
    0으로 나눌 때 발생하는 ZeroDivisionError를 잡아 시스템 충돌을 방지합니다.
    """
    try:
        result = numerator / denominator
        return result
    except ZeroDivisionError:
        print("[경고] 0으로 나눌 수 없어 0.0을 안전하게 반환합니다.")
        return 0.0
    except TypeError as e:
        print(f"[경고] 숫자가 아닌 타입이 들어왔습니다: {e}")
        return 0.0


# =====================================================================
# 3. 파일 입출력 (CSV 파일 생성 및 읽기)
# =====================================================================
def create_sample_dataset_csv(filepath: Path):
    """with open 문을 사용하여 안전하게 CSV 파일 작성"""
    sample_data = [
        ["student_id", "name", "math", "python", "status"],
        ["S001", "홍길동", 85, 92, "PASS"],
        ["S002", "이순신", 95, 88, "PASS"],
        ["S003", "강감찬", 45, 55, "FAIL"],
        ["S004", "신사임당", 100, 98, "PASS"],
    ]

    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(sample_data)
    print(f"[INFO] 샘플 CSV 파일 생성 완료: {filepath}")


def read_dataset_csv(filepath: Path) -> list:
    """생성된 CSV 파일을 읽어 딕셔너리 리스트로 변환"""
    records = []
    if not filepath.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {filepath}")

    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 문자열 숫자를 정수로 형변환
            row["math"] = int(row["math"])
            row["python"] = int(row["python"])
            row["avg_score"] = round((row["math"] + row["python"]) / 2, 1)
            records.append(row)

    return records


def main():
    # 1. 함수 실행 (*kwargs 전달)
    model_res = calculate_model_score(
        base_acc=0.88,
        bonus=0.05,
        dataset="credit_fraud_v2",
        author="kdw",
        is_best=True
    )

    # 2. 예외 처리 실행
    div_ok = safe_divide(100, 4)
    div_err = safe_divide(100, 0) # 0 나누기 예외 처리 작동

    # 3. 파일 입출력 실행
    csv_path = Path(__file__).resolve().parent.parent / "data" / "sample_students.csv"
    create_sample_dataset_csv(csv_path)
    student_records = read_dataset_csv(csv_path)

    # 4. 터미널 출력
    if HAS_RICH and console:
        console.print(Panel.fit("[bold magenta]⚙️ 02강 기초 3편: 함수, 예외 처리, 파일 I/O[/bold magenta]"))

        # 함수 결과
        console.print(f"1. **calculate_model_score() 실행 결과**: {model_res}")
        console.print(f"2. **safe_divide() 결과**: 100/4={div_ok}, 100/0={div_err}")

        # CSV 읽은 결과 테이블
        table_csv = Table(title="3. CSV 파일 읽기 & 평균 점수 계산 결과", header_style="bold cyan")
        table_csv.add_column("학번", justify="center")
        table_csv.add_column("이름")
        table_csv.add_column("수학", justify="right")
        table_csv.add_column("파이썬", justify="right")
        table_csv.add_column("평균 점수", justify="right", style="bold green")
        table_csv.add_column("상태", justify="center")

        for row in student_records:
            status_style = "bold green" if row["status"] == "PASS" else "bold red"
            table_csv.add_row(
                row["student_id"],
                row["name"],
                str(row["math"]),
                str(row["python"]),
                str(row["avg_score"]),
                f"[{status_style}]{row['status']}[/{status_style}]"
            )
        console.print(table_csv)

    else:
        print(f"모델 점수: {model_res}")
        print(f"안전 나누기: {div_ok}, {div_err}")
        print(f"학생 데이터 {len(student_records)}건 로드 완료")


if __name__ == "__main__":
    main()
