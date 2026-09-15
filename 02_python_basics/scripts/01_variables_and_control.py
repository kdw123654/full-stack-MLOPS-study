"""
[MLOps Full-Stack 02강] 01_variables_and_control.py
- 파이썬의 가장 기초적인 문법: 변수, 자료형, 연산자, 조건문, 반복문
"""

import sys

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


def demonstrate_variables_and_types():
    """1. 변수와 기본 데이터 타입"""
    # 파이썬은 변수 선언 시 타입을 명시하지 않아도 값에 따라 자동으로 결정됩니다 (동적 타이핑)
    user_name = "김파이썬"          # str (문자열)
    user_age = 28                  # int (정수)
    accuracy_score = 0.9542        # float (부동소수점 실수)
    is_model_trained = True        # bool (불리언: True / False)

    # f-string: 변수를 문자열 안에 깔끔하게 출력하는 최신 방법
    summary = f"이름: {user_name}, 나이: {user_age}세, 모델 정확도: {accuracy_score * 100:.2f}%, 학습 완료: {is_model_trained}"
    
    # 형변환 (Type Casting)
    str_num = "100"
    converted_int = int(str_num)   # 문자열 "100" -> 정수 100
    float_num = float(converted_int) # 정수 100 -> 실수 100.0

    return {
        "summary": summary,
        "types": [
            ("user_name", str(user_name), str(type(user_name))),
            ("user_age", str(user_age), str(type(user_age))),
            ("accuracy_score", str(accuracy_score), str(type(accuracy_score))),
            ("is_model_trained", str(is_model_trained), str(type(is_model_trained))),
            ("converted_int", str(converted_int), str(type(converted_int))),
            ("float_num", str(float_num), str(type(float_num))),
        ]
    }


def demonstrate_conditional_statements(score: float):
    """2. 조건문 (if, elif, else)"""
    # 점수에 따른 모델 성능 판정 로직
    if score >= 0.90:
        evaluation = "🏆 우수 모델 (배포 승인 가능)"
        color = "green"
    elif score >= 0.70:
        evaluation = "⚠️ 보통 모델 (하이퍼파라미터 튜닝 필요)"
        color = "yellow"
    else:
        evaluation = "❌ 부적합 모델 (데이터 추가 수집 필요)"
        color = "red"

    return evaluation, color


def demonstrate_loops():
    """3. 반복문 (for문과 while문)"""
    # for문과 range()를 사용한 에포크(Epoch) 학습 시뮬레이션
    training_logs = []
    loss = 1.0

    for epoch in range(1, 6): # 1부터 5까지 반복
        loss *= 0.6 # 학습할 때마다 손실(Loss)이 감소한다고 가정
        training_logs.append((epoch, f"{loss:.4f}"))

    # enumerate(): 인덱스와 요소를 동시에 가져오는 필수 내장 함수
    model_candidates = ["Logistic Regression", "Random Forest", "XGBoost", "LightGBM"]
    ranking_logs = []
    for rank, model_name in enumerate(model_candidates, start=1):
        ranking_logs.append((rank, model_name))

    return training_logs, ranking_logs


def main():
    var_res = demonstrate_variables_and_types()
    score = 0.92
    eval_text, eval_color = demonstrate_conditional_statements(score)
    train_logs, rank_logs = demonstrate_loops()

    if HAS_RICH and console:
        console.print(Panel.fit("[bold green]🐍 02강 기초 1편: 변수, 자료형, 조건문, 반복문[/bold green]"))

        # 1. 자료형 표
        table_vars = Table(title="1. 파이썬 핵심 기본 자료형", header_style="bold cyan")
        table_vars.add_column("변수명", style="dim")
        table_vars.add_column("값", style="bold")
        table_vars.add_column("파이썬 타입 (type)")
        for name, val, typ in var_res["types"]:
            table_vars.add_row(name, val, typ)
        console.print(table_vars)

        # 2. 조건문 결과
        console.print(f"\n[bold]2. 모델 성능 평가 (점수: {score})[/bold]: [{eval_color}]{eval_text}[/{eval_color}]")

        # 3. 반복문 결과
        table_train = Table(title="3. for문 반복 학습 시뮬레이션 (Epoch & Loss)", header_style="bold magenta")
        table_train.add_column("Epoch", justify="center")
        table_train.add_column("Loss (손실값)", justify="right")
        for ep, ls in train_logs:
            table_train.add_row(f"Epoch {ep}", ls)
        console.print(table_train)

    else:
        print("=== 1. 변수와 타입 ===")
        print(var_res["summary"])
        print("\n=== 2. 조건문 평가 ===")
        print(f"점수 {score} -> {eval_text}")
        print("\n=== 3. 반복문 로그 ===")
        for ep, ls in train_logs:
            print(f"Epoch {ep}: Loss {ls}")


if __name__ == "__main__":
    main()
