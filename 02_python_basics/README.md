# 📖 [제2강] 파이썬 기초 바닥부터 완전 정복 (Core Fundamentals)

> **"아무리 높은 빌딩도 기초 공사가 부실하면 무너집니다.  
> MLOps 풀스택의 거대한 파이프라인을 지탱할 가장 단단한 파이썬 코어 기본기를 다집니다."**

---

## 🎯 이번 강의 학습 목표
1. **변수(Variable)와 4대 기본 자료형(`int`, `float`, `str`, `bool`)**의 메모리 동작 원리를 이해하고 **f-string** 포맷팅을 능숙하게 사용한다.
2. **조건문(`if-elif-else`)과 반복문(`for`, `while`)**을 조합하여 프로그램의 제어 흐름을 설계한다.
3. 파이썬의 꽃이라 불리는 **4대 컬렉션 자료구조(`List`, `Tuple`, `Dictionary`, `Set`)**의 특성을 비교하고, **리스트 컴프리헨션(List Comprehension)**을 익힌다.
4. **함수(`def`)**의 입력(`*args`, `**kwargs`)과 출력(`return`) 구조를 마스터하여 코드를 모듈화한다.
5. 시스템 충돌을 방지하는 **예외 처리(`try-except`)**와 안전한 **파일 입출력(`with open`, CSV)**을 체화한다.

---

## 1. 파이썬의 기본 철학: 변수와 자료형

### 1.1 변수(Variable)란?
변수는 컴퓨터 메모리(RAM)의 특정 위치에 **이름표(Label)**를 붙여두고 데이터를 담아두는 상자입니다.  
파이썬은 타입을 미리 지정하지 않아도 대입되는 값에 따라 타입이 자동으로 결정되는 **동적 타이핑(Dynamic Typing)** 언어입니다.

```python
age = 28               # int (정수)
accuracy = 0.954       # float (실수)
model_name = "XGBoost" # str (문자열)
is_trained = True      # bool (참/거짓)
```

### 1.2 형변환 (Type Casting)의 중요성
웹 브라우저(프론트엔드)나 파일(CSV)에서 데이터를 읽어오면 숫자가 아닌 문자열 `"100"`으로 들어옵니다. 이를 계산하려면 반드시 형변환을 거쳐야 합니다:
```python
raw_input = "100"
converted = int(raw_input)   # 문자열 -> 정수 100
float_val = float(converted) # 정수 -> 실수 100.0
text_val = str(float_val)    # 실수 -> 문자열 "100.0"
```

### 1.3 f-string: 가장 우아한 문자열 출력법
과거의 `%` 연산자나 `.format()` 대신, Python 3.6부터 도입된 **f-string**을 무조건 사용하는 것이 실무 표준입니다:
```python
name = "홍길동"
score = 98.7654

# 문자열 앞에 f를 붙이고 중괄호 {} 안에 변수나 표현식을 넣습니다.
print(f"학생: {name}, 최종 점수: {score:.2f}점") # 소수점 둘째 자리까지: 98.77점
```

---

## 2. 연산자와 제어문 (조건문 & 반복문)

### 2.1 조건문 (`if`, `elif`, `else`)
조건문은 특정 조건이 참(`True`)일 때만 코드를 실행하도록 흐름을 분기합니다.

```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"
```
> **논리 연산자**: `and`(둘 다 참), `or`(하나라도 참), `not`(반대)

### 2.2 반복문 (`for`, `while`)

#### 1) `for`문과 `range()`
정해진 횟수만큼 반복할 때 가장 많이 쓰입니다:
```python
# 0부터 4까지 5회 반복
for i in range(5):
    print(f"에포크 {i + 1}회차 학습 진행 중...")
```

#### 2) `enumerate()`: 인덱스와 요소를 한 번에!
리스트를 순회할 때 번호(인덱스)가 함께 필요하다면 `enumerate()`를 사용합니다:
```python
models = ["ResNet", "BERT", "GPT"]
for idx, model in enumerate(models, start=1):
    print(f"{idx}위 모델: {model}")
```

#### 3) `while`문과 `break`, `continue`
- `break`: 반복문을 즉시 탈출
- `continue`: 다음 반복 회차로 건너뜀

---

## 3. 파이썬 4대 핵심 자료구조

데이터 분석과 머신러닝의 90%는 이 4가지 자료구조를 가공하는 작업입니다.

| 자료구조 | 표기법 | 순서 | 수정 가능(Mutable) | 중복 허용 | 주요 사용처 |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **List** | `[1, 2, 3]` | O | O | O | 순차적 데이터, 피처 목록 |
| **Tuple** | `(1, 2, 3)` | O | X (불변) | O | 좌표, 이미지 크기 `(H, W, C)` |
| **Dictionary**| `{"a": 1}` | O (3.7+) | O | Key 중복 불가 | JSON, 메트릭, 설정값 |
| **Set** | `{1, 2, 3}` | X | O | X (중복 불가) | 유니크 ID 추출, 교집합/합집합 |

### 3.1 리스트 슬라이싱 (Slicing) 완벽 정리
문법: `list[시작:끝:증감폭]` (끝 인덱스는 포함되지 않음)
```python
nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

nums[:3]    # [0, 1, 2] (처음부터 3개)
nums[7:]    # [7, 8, 9] (7번부터 끝까지)
nums[-1]    # 9 (맨 마지막 1개)
nums[::-1]  # [9, 8, ..., 0] (역순 뒤집기)
```

### 3.2 딕셔너리의 생존 치트키: `.get()`
딕셔너리에서 존재하지 않는 키를 `dict["key"]`로 접근하면 서버가 에러(`KeyError`)를 뿜으며 멈춥니다.  
반드시 `.get()` 메서드를 사용하여 안전하게 기본값을 지정하세요:
```python
metrics = {"accuracy": 0.92}

# 안전한 접근 (키가 없으면 None 또는 기본값 반환)
acc = metrics.get("accuracy")         # 0.92
loss = metrics.get("loss", 0.0)       # 키가 없으므로 0.0 반환 (에러 없음!)
```

### 3.3 리스트 컴프리헨션 (List Comprehension)
파이썬의 가장 아름다운 문법으로, 리스트 안에서 반복문과 조건문을 한 줄로 작성해 새로운 리스트를 만듭니다.

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 짝수만 골라서 제곱하기
# [연산식 for 반복변수 in 대상 if 조건문]
even_squares = [x ** 2 for x in numbers if x % 2 == 0]
# 결과: [4, 16, 36, 64, 100]
```

---

## 4. 함수(Function)와 모듈화

반복되는 코드를 하나로 묶어 이름을 붙인 것을 함수라고 합니다.

```python
def predict_churn(customer_id: str, tenure: int, monthly_bill: float) -> dict:
    """고객 이탈 확률을 계산하는 함수"""
    risk_score = (monthly_bill / 100) * (1 / (tenure + 1))
    is_churn = risk_score > 0.5
    return {
        "id": customer_id,
        "is_churn": is_churn,
        "risk": round(risk_score, 3)
    }
```

### 가변 인자: `*args`와 `**kwargs`
- `*args`: 몇 개가 들어올지 모르는 위치 인자를 **튜플(tuple)**로 받음
- `**kwargs`: 키=값 형태로 들어오는 인자들을 **딕셔너리(dict)**로 받음

---

## 5. 예외 처리와 파일 입출력

### 5.1 예외 처리 (`try - except - finally`)
예기치 못한 에러가 발생해도 프로그램이 강제 종료되지 않고 우아하게 복구되도록 보호합니다:
```python
try:
    result = 100 / 0 # 위험한 코드
except ZeroDivisionError as e:
    print(f"0으로 나눌 수 없습니다: {e}")
    result = 0.0
finally:
    print("성공/실패 여부와 관계없이 항상 마지막에 실행되는 블록")
```

### 5.2 `with open`을 이용한 파일 입출력
파일을 열고 깜빡 잊고 닫지(`f.close()`) 않으면 메모리 누수나 파일 손상이 일어납니다.  
`with open` 구문을 쓰면 블록이 끝날 때 **파이썬이 파일을 자동으로 닫아줍니다**:
```python
# 1. 파일 쓰기
with open("result.txt", "w", encoding="utf-8") as f:
    f.write("모델 학습 완료: Accuracy 95%\n")

# 2. 파일 읽기
with open("result.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)
```

---

## 6. 실습 실행 가이드

터미널에서 아래 3개의 실습 스크립트를 순서대로 실행해 보세요:

```powershell
# 프로젝트 루트(mlops full-stack)에서 실행

# 1. 변수, 자료형, 조건문, 반복문 실습
python 02_python_basics/scripts/01_variables_and_control.py

# 2. 4대 자료구조와 컴프리헨션 실습
python 02_python_basics/scripts/02_data_structures.py

# 3. 함수, 예외 처리, CSV 파일 입출력 실습
python 02_python_basics/scripts/03_functions_and_file_io.py
```

---

## 7. 제2강 실습 과제
개념을 모두 익히셨다면, [2강 과제 가이드](assignments/homework_02.md)를 열고 나만의 학생 성적 분석기를 직접 코딩해 보세요!
