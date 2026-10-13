# 📖 [제5강] 프로덕션 데이터 파이프라인 (Pandas & Polars, 데이터 품질 검증)

> **"쓰레기 데이터(Garbage In)가 들어가면 아무리 화려한 딥러닝 모델도 쓰레기 예측(Garbage Out)을 뱉습니다.  
> MLOps 엔지니어의 핵심 경쟁력은 '재현 가능하고(Reproducible) 대용량 트래픽에도 빠른 데이터 파이프라인'을 구축하는 것입니다."**

---

## 🎯 이번 강의 학습 목표
1. 주피터 노트북의 파편화된 전처리에서 벗어나, **클래스와 모듈로 캡슐화된 프로덕션 전처리 파이프라인**을 설계한다.
2. 결측치(Missing Values) 처리의 다양한 기법(중앙값, 평균, 최빈값)과 **이상치(Outlier) 필터링 전략**을 체화한다.
3. 데이터 과학의 오랜 표준 **Pandas**와 Rust 기반의 차세대 초고속 프레임워크 **Polars**의 차이점을 완벽히 이해한다.
4. Polars의 **`LazyFrame` 지연 평가(Lazy Evaluation)**와 **Apache Parquet** 컬럼 기반 압축 포맷을 실무에 적용한다.
5. 모델 학습과 배포 전에 데이터의 오염 여부를 사전 탐지하는 **데이터 계약(Data Contract) 및 품질 검증기**를 구축한다.

---

## 1. 왜 프로덕션 데이터 파이프라인인가?

### 1.1 노트북 전처리의 치명적 한계
많은 초보자가 다음과 같은 방식으로 데이터를 다룹니다:
```python
# ❌ 주피터 노트북에서 흔히 하는 실수
df = df.dropna()                     # 중요 데이터 날려먹기
df['age'] = df['age'].fillna(30)     # 임의의 숫자 하드코딩
# 셀 실행 순서가 꼬이면 결과가 매번 달라짐!
```
- 모델이 실시간 서빙될 때(API로 1건씩 들어올 때) 이 코드를 재사용할 수 없습니다.
- 학습할 때 사용한 전처리 통계량(평균값, 중앙값)이 어딘가에 저장되지 않아 **학습-서빙 불일치(Skew)**가 발생합니다.

### 1.2 프로덕션 파이프라인의 4단계
```
[ 1. 원본 데이터 수집 ] ──► [ 2. 이상치/결측치 정제 ] ──► [ 3. 피처 엔지니어링 ] ──► [ 4. 데이터 품질 검증 ]
 (CSV, Parquet, DB)        (IQR, Median Imputation)      (One-Hot, Scaling)          (Schema, Null Threshold)
```

---

## 2. Pandas 전처리 파이프라인 실무

### 2.1 결측치(Imputation) 전략
무조건 행을 삭제(`dropna`)하는 것은 데이터 손실이 크므로 위험합니다:
- **연속형 숫자(Age, Income)**: 극단값의 영향을 덜 받는 **중앙값(Median)** 또는 평균(Mean) 대체
- **범주형 문자(Tier, Grade)**: 가장 빈도가 높은 **최빈값(Mode)** 또는 `"UNKNOWN"` 플래그 부여

### 2.2 이상치(Outlier) 처리
- **도메인 규칙 필터링**: 나이가 0세 미만이거나 120세 초과인 경우, 구매 금액이 음수인 경우 등 물리적으로 불가능한 값을 탐지하여 `NaN`으로 변환 후 보정합니다.

---

## 3. 차세대 데이터 처리의 표준: Polars (폴라즈)

### 3.1 왜 지금 Polars인가?
- **Pandas**: Python과 C로 작성되었으며, 기본적으로 **단일 CPU 코어(Single-thread)**만 사용합니다. 데이터가 수 기가바이트(GB)를 넘어가면 메모리 부족(OOM)으로 터집니다.
- **Polars**: 최신 시스템 언어인 **Rust**로 바닥부터 작성되었으며, 컴퓨터의 **모든 CPU 코어를 100% 병렬 활용(Multi-threaded)**합니다. Pandas 대비 **5배 ~ 20배 빠르고 메모리를 1/3만 사용**합니다.

| 기능 비교 | Pandas | Polars |
| :--- | :--- | :--- |
| **코어 엔진** | Python + C | Rust + Apache Arrow |
| **병렬 처리** | 기본 단일 코어 | 기본 멀티스레드 병렬 |
| **지연 평가(Lazy)**| 미지원 (즉시 계산) | 지원 (`LazyFrame`) |
| **대용량 데이터** | 메모리 부족 자주 발생 | 쿼리 플래너 최적화로 안정적 |

### 3.2 Polars의 핵심: `LazyFrame`과 지연 평가 (Lazy Evaluation)
일반 판다스는 코드를 한 줄 실행할 때마다 즉시 메모리에 데이터를 올립니다.  
반면 Polars는 쿼리를 쭉 쌓아둔 뒤(`scan_csv` -> `filter` -> `with_columns`), 마지막에 `collect()`를 호출할 때 **쿼리 최적화기(Optimizer)가 가장 빠른 경로로 한 번에 연산**합니다:

```python
import polars as pl

# 1. 쿼리 계획만 세움 (데이터 메모리 적재 X)
q = (
    pl.scan_csv("data.csv")
    .filter(pl.col("age") >= 20)
    .select(["user_id", "purchase_amount"])
)

# 2. 최적화된 엔진으로 일괄 연산 실행!
df = q.collect()
```

### 3.3 CSV vs Apache Parquet 비교
MLOps에서는 용량이 크고 읽기 느린 CSV 대신 **Parquet(파케이)** 포맷을 표준으로 씁니다:
- **압축률**: CSV 대비 용량이 **1/4 ~ 1/10** 수준으로 줄어듦
- **데이터 타입 보존**: CSV는 읽을 때마다 타입을 추론해야 하지만, Parquet은 파일 자체에 int, float 스키마가 완벽히 보존됨

---

## 4. 데이터 계약(Data Contract)과 품질 검증

아무리 좋은 모델도 입력 데이터의 스키마가 깨지면 즉사합니다.  
우리는 `DataQualityValidator`를 구축하여 다음을 자동으로 감시합니다:
1. **필수 컬럼 누락 여부 (Missing Columns)**
2. **컬럼별 결측치 비율 (Null Ratio Threshold, 예: 10% 초과 시 경고)**
3. **수치형 데이터 범위 위반 (음수 값 감지 등)**

---

## 5. 실습 실행 가이드

터미널에서 아래 순서대로 실행해 보세요:

```powershell
# 1. 5강 필수 패키지 설치
cd 05_production_data_pipeline
pip install -r requirements.txt

# 2. 원본 노이즈/결측치 데이터셋 1000건 생성
python scripts/generate_sample_data.py

# 3. Pandas 모듈형 전처리 파이프라인 가동
python scripts/01_pandas_pipeline.py

# 4. Polars 초고속 Lazy 파이프라인 & Parquet 저장 가동
python scripts/02_polars_pipeline.py

# 5. 데이터 계약 및 품질 검증기 실행
python scripts/03_data_validator.py
```

---

## 6. 제5강 실습 과제
이론과 실습을 마쳤다면, [5강 과제 가이드](assignments/homework_05.md)를 열어 금융 신용카드 거래 데이터의 이상치 정제 파이프라인을 완성해 보세요!
