# 📖 [제3강] 모던 파이썬 & 객체지향 설계(OOP) 및 Pydantic 데이터 검증

> **"Garbage In, Garbage Out (쓰레기가 들어가면 쓰레기가 나온다).  
> MLOps 엔지니어의 첫 번째 사명은 비정상 데이터가 모델에 닿기 전에 시스템 레벨에서 원천 차단하는 것입니다."**

---

## 🎯 이번 강의 학습 목표
1. **타입 힌팅(`typing`)**을 체화하여 런타임 버그를 사전에 차단하고 IDE의 자동완성 생산성을 극대화한다.
2. 데이터 과학자의 스파게티 스크립트에서 벗어나, **추상 클래스(ABC)와 팩토리 패턴**을 적용한 재사용 가능한 OOP 파이프라인을 설계한다.
3. 머신러닝 하이퍼파라미터 및 설정을 안전하게 관리하는 **불변 데이터 클래스(`dataclass(frozen=True)`)**를 활용한다.
4. FastAPI 및 프로덕션 MLOps의 표준 데이터 검증 라이브러리인 **Pydantic v2**의 핵심 기능(`BaseModel`, `Field`, `@field_validator`, `@model_validator`)을 완벽히 마스터한다.
5. 모델 서빙 시 발생할 수 있는 이상치와 결측치를 사전에 탐지하고 차단하는 실무 검증 파이프라인을 구축한다.

---

## 1. 왜 MLOps에서 "모던 파이썬"과 "OOP"가 필수인가?

### 1.1 데이터 과학자의 스크립트 vs MLOps 엔지니어의 코드
주피터 노트북(`.ipynb`)에서 실험할 때는 아래와 같은 코드를 작성해도 큰 문제가 없습니다:

```python
# ❌ 전형적인 노트북 스파게티 코드
def prep(d):
    d['a'] = d['a'].fillna(0)
    return d / 100

data = load()
res = prep(data)
```

하지만 이 코드가 **하루에 수만 건의 API 요청을 처리하는 실시간 서빙 서버**로 올라가면 대재앙이 일어납니다:
- `d`가 딕셔너리인지, 판다스 데이터프레임인지, 리스트인지 알 수 없습니다.
- 컬럼 이름 `'a'`가 `'A'`로 바뀌거나, 문자열 `"N/A"`가 들어오면 서버 전체가 `TypeError`로 뻗어버립니다.
- 전처리 로직이 함수 단위로 파편화되어 모델 학습 때 쓴 전처리와 서빙 때 쓴 전처리가 불일치하는 **학습-서빙 불일치(Training-Serving Skew)**가 발생합니다.

### 1.2 MLOps 풀스택의 해결책
1. **정적 타입 명시 (Type Hints)**: 입력과 출력의 형태를 엄격하게 정의합니다.
2. **객체지향 모듈화 (OOP)**: Scikit-Learn처럼 `fit()`, `transform()` 규격을 통일합니다.
3. **스키마 검증 (Pydantic)**: 서빙 API 문앞에 엄격한 문지기(Validator)를 배치합니다.

---

## 2. 모던 파이썬 타입 힌팅 (Type Hinting) 실무

Python 3.10 이상부터는 더욱 간결하고 강력한 타입 문법을 지원합니다.

### 2.1 핵심 타입 문법 비교
| 용도 | 과거 문법 (Python 3.8 이하) | 모던 문법 (Python 3.10+) | 설명 |
| :--- | :--- | :--- | :--- |
| **리스트** | `from typing import List`<br>`List[float]` | `list[float]` | 부동소수점 숫자 리스트 |
| **딕셔너리** | `from typing import Dict`<br>`Dict[str, int]` | `dict[str, int]` | 문자열 키, 정수 값 매핑 |
| **선택적(None 허용)** | `from typing import Optional`<br>`Optional[str]` | `str \| None` | 문자열 또는 None 허용 |
| **유니온(다중 타입)** | `from typing import Union`<br>`Union[int, float]` | `int \| float` | 정수 또는 실수 |
| **고정된 선택지** | `from typing import Literal`<br>`Literal["cpu", "cuda"]` | 동일 | 정해진 문자열 리터럴만 허용 |

### 2.2 실무 팁: `typing.Annotated`
타입에 메타데이터(설명, 단위 등)를 결합할 때 매우 유용합니다:
```python
from typing import Annotated

# 속도 (단위: km/h, 최댓값 300)
SpeedKmH = Annotated[float, "단위: km/h, max: 300.0"]
```

---

## 3. 객체지향 설계(OOP)와 파이프라인 패턴

### 3.1 추상 기반 클래스 (Abstract Base Class, ABC)
새로운 전처리 알고리즘(예: RobustScaler, LogTransformer)이 추가되더라도 기존 코드를 수정할 필요 없이 동일한 규격을 강제하기 위해 `abc.ABC`를 사용합니다:

```python
from abc import ABC, abstractmethod

class BasePreprocessor(ABC):
    @abstractmethod
    def fit(self, data: list[float]) -> "BasePreprocessor":
        """데이터의 통계량(평균, 편차 등)을 학습합니다."""
        pass

    @abstractmethod
    def transform(self, data: list[float]) -> list[float]:
        """학습된 통계량으로 데이터를 변환합니다."""
        pass
```

### 3.2 팩토리 패턴 (Factory Pattern)
설정 파일의 문자열(`"standard"`, `"minmax"`)만 보고 적절한 전처리 객체를 동적으로 생성해 주는 디자인 패턴입니다.  
(`01_type_hints_and_oop.py` 파일의 `PreprocessorFactory` 구현을 참고하세요.)

---

## 4. MLOps의 방패: Pydantic v2 완벽 정복

### 4.1 왜 `dataclass`나 `dict`만으로 부족한가?
- Python 기본 `dataclass`나 `dict`는 **타입 검사를 강제하지 않습니다.** (타입 힌트에 `int`라고 적혀 있어도 문자열 `"abc"`를 넣으면 그냥 들어갑니다.)
- **Pydantic**은 런타임에 데이터를 파싱하고, 타입 변환(Coercion)을 시도하며, 제약 조건에 어긋나면 즉시 상세한 에러(`ValidationError`)를 발생시킵니다.
- FastAPI의 모든 요청(Request) / 응답(Response) 모델이 바로 Pydantic으로 동작합니다!

### 4.2 Pydantic 핵심 문법

#### 1) `BaseModel`과 `Field`
```python
from pydantic import BaseModel, Field

class IrisFeature(BaseModel):
    sepal_length: float = Field(..., ge=0.0, le=10.0, description="꽃받침 길이 (0~10cm)")
    sepal_width: float = Field(..., ge=0.0, le=10.0)
    species_name: str = Field(default="unknown")
```
- `...` (Ellipsis): **필수 입력 필드**임을 의미합니다.
- `ge` (Greater than or Equal): 이상 (>=)
- `le` (Less than or Equal): 이하 (<=)
- `default`: 기본값 지정

#### 2) 필드 단위 커스텀 검증 (`@field_validator`)
특정 필드에 특수한 도메인 규칙이 필요할 때 사용합니다:
```python
from pydantic import field_validator

class UserInput(BaseModel):
    email: str

    @field_validator("email")
    @classmethod
    def check_company_email(cls, v: str) -> str:
        if not v.endswith("@company.com"):
            raise ValueError("회사 전용 이메일(@company.com)만 허용됩니다.")
        return v
```

#### 3) 복합 필드 간 논리 검증 (`@model_validator(mode="after")`)
여러 필드를 결합하여 논리적 모순을 잡아야 할 때 사용합니다:
```python
from pydantic import model_validator

class ServiceSubscription(BaseModel):
    tenure_months: int  # 가입 개월 수
    total_bill: float   # 누적 요금

    @model_validator(mode="after")
    def validate_logic(self) -> "ServiceSubscription":
        # 가입 개월이 0인데 요금이 청구되었는지 검사
        if self.tenure_months == 0 and self.total_bill > 0:
            raise ValueError("0개월 차 신규 회원은 누적 요금이 0원이어야 합니다.")
        return self
```

---

## 5. 실습 코드 실행 안내

### 실습 1: 타입 힌트 & OOP 전처리기 팩토리
```powershell
# 프로젝트 루트(mlops full-stack)에서 실행
python 02_modern_python_and_pydantic/scripts/01_type_hints_and_oop.py
```
- 불변 설정 관리(`dataclass(frozen=True)`) 동작 확인
- `StandardScaler`, `MinMaxScaler`의 통일된 `fit_transform` 파이프라인 확인

### 실습 2: Pydantic v2 데이터 검증 및 이상치 차단
```powershell
python 02_modern_python_and_pydantic/scripts/02_pydantic_validation.py
```
- 정상 고객 데이터의 완벽한 배치 파싱 확인
- 나이 제한 위반, 접두사 누락, 0개월 차 요금 발생 모순 등이 **어떻게 실시간으로 걸러지는지** 에러 테이블 확인!

---

## 6. MLOps 실무 FAQ

### Q1. `dataclass`와 `Pydantic BaseModel`은 언제 각각 써야 하나요?
- **`dataclass`를 쓸 때**: 내부 모듈 간의 단순 파라미터 전달, 가벼운 불변 설정 객체(`frozen=True`), 외부 입력 검증이 필요 없을 때.
- **`Pydantic BaseModel`을 쓸 때**: 외부 세계(사용자 브라우저, 프론트엔드, API 클라이언트, 환경 변수 `.env`)로부터 들어오는 데이터를 파싱하고 검증할 때. (FastAPI와의 결합 시 필수)

### Q2. Pydantic v1을 썼었는데 v2에서 무엇이 가장 크게 달라졌나요?
- Pydantic v2는 코어 엔진이 **Rust**로 재작성되어 검증 속도가 최대 5~10배 빨라졌습니다.
- 데코레이터가 `@validator` -> `@field_validator`, `@root_validator` -> `@model_validator`로 변경되었습니다. (본 레포지토리는 최신 v2 표준 문법을 따릅니다.)

---

## 7. 제3강 실습 과제
이론과 코드를 확인하셨다면, [3강 과제 가이드](assignments/homework_03.md)를 열어 나만의 센서 데이터 검증 스키마를 구현해 보세요!
