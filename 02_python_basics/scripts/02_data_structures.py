"""
[MLOps Full-Stack 02강] 02_data_structures.py
- 파이썬의 4대 핵심 자료구조: List, Tuple, Dictionary, Set
- 데이터 분석과 ML 전처리의 핵심: 리스트 컴프리헨션 (List Comprehension)
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


def demonstrate_list_and_slicing():
    """1. 리스트(List)와 슬라이싱(Slicing)"""
    features = ["age", "income", "tenure", "balance", "credit_score"]
    
    # 추가, 삭제
    features.append("country")      # 맨 뒤에 추가
    removed_item = features.pop(1)  # 1번 인덱스("income") 꺼내서 제거
    
    # 슬라이싱 (매우 중요!)
    first_two = features[:2]        # 앞에서부터 2개
    last_item = features[-1]        # 맨 마지막 1개
    reversed_features = features[::-1] # 역순 뒤집기

    return {
        "current_list": features,
        "first_two": first_two,
        "last_item": last_item,
        "removed_item": removed_item
    }


def demonstrate_dictionary():
    """2. 딕셔너리(Dictionary): Key - Value 매핑"""
    # 머신러닝 모델 메트릭 저장 예시
    model_metrics = {
        "model_name": "RandomForestClassifier",
        "accuracy": 0.892,
        "f1_score": 0.875,
        "parameters": {"n_estimators": 100, "max_depth": 10}
    }

    # 안전하게 값 가져오기 (.get) - 키가 없어도 KeyError 에러 대신 None 반환
    f1 = model_metrics.get("f1_score")
    precision = model_metrics.get("precision", "N/A (미측정)") # 기본값 지정 가능

    return model_metrics, f1, precision


def demonstrate_tuple_and_set():
    """3. 튜플(Tuple)과 세트(Set)"""
    # 튜플: 수정 불가능(Immutable), 좌표나 고정 메타데이터에 사용
    image_shape = (224, 224, 3) # (높이, 너비, 채널 수)
    height, width, channels = image_shape # 언패킹(Unpacking)

    # 세트: 중복 제거 및 집합 연산
    raw_user_ids = ["USER-1", "USER-2", "USER-1", "USER-3", "USER-2", "USER-4"]
    unique_user_ids = set(raw_user_ids) # 중복이 자동으로 날아감!

    return (height, width, channels), list(unique_user_ids)


def demonstrate_list_comprehension():
    """4. 리스트 컴프리헨션(List Comprehension) - 파이써닉 코드의 정수"""
    raw_scores = [45, 82, 95, 60, 38, 77, 90]

    # [전통적인 방식: 4줄]
    # passed_scores = []
    # for s in raw_scores:
    #     if s >= 60:
    #         passed_scores.append(s * 1.1)

    # [리스트 컴프리헨션: 단 1줄]
    # 60점 이상인 점수만 골라서 10% 가산점 부여
    boosted_scores = [round(s * 1.1, 1) for s in raw_scores if s >= 60]

    # 딕셔너리 컴프리헨션: 리스트를 바탕으로 키-값 딕셔너리 즉시 생성
    label_mapping = {f"Class_{i}": val for i, val in enumerate(["Dog", "Cat", "Bird"])}

    return raw_scores, boosted_scores, label_mapping


def main():
    list_info = demonstrate_list_and_slicing()
    metrics, f1, prec = demonstrate_dictionary()
    img_shape, unique_ids = demonstrate_tuple_and_set()
    raw_sc, boosted_sc, labels = demonstrate_list_comprehension()

    if HAS_RICH and console:
        console.print(Panel.fit("[bold cyan]📚 02강 기초 2편: 핵심 자료구조 & 컴프리헨션[/bold cyan]"))

        # 1. 딕셔너리 테이블
        table_dict = Table(title="1. 머신러닝 메트릭 딕셔너리 (.get 활용)", header_style="bold yellow")
        table_dict.add_column("Key (항목)")
        table_dict.add_column("Value (값)", style="bold")
        for k, v in metrics.items():
            table_dict.add_row(k, str(v))
        table_dict.add_row("precision (없는 키 .get 조회)", str(prec), style="dim")
        console.print(table_dict)

        # 2. 리스트 컴프리헨션 비교
        table_comp = Table(title="2. 리스트 컴프리헨션 (60점 이상 10% 가산점)", header_style="bold green")
        table_comp.add_column("원본 점수 리스트", style="dim")
        table_comp.add_column("컴프리헨션 필터링 & 연산 결과", style="bold green")
        table_comp.add_row(str(raw_sc), str(boosted_sc))
        console.print(table_comp)

        # 3. 튜플 언패킹 및 Set 중복 제거
        console.print(f"\n[bold]3. 튜플 언패킹 결과[/bold]: 높이={img_shape[0]}px, 너비={img_shape[1]}px, 채널={img_shape[2]}")
        console.print(f"[bold]4. Set으로 중복 제거된 유니크 ID 수[/bold]: {len(unique_ids)}개 ({unique_ids})")

    else:
        print("=== 1. 리스트와 슬라이싱 ===")
        print(f"현재 리스트: {list_info['current_list']}")
        print(f"앞 2개: {list_info['first_two']}, 마지막: {list_info['last_item']}")
        print("\n=== 2. 딕셔너리 ===")
        print(f"F1 Score: {f1}, Precision: {prec}")
        print("\n=== 3. 컴프리헨션 ===")
        print(f"원본: {raw_sc}")
        print(f"변환: {boosted_sc}")


if __name__ == "__main__":
    main()
