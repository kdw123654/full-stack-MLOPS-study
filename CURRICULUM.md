# 📋 MLOps Full-Stack Master Curriculum (상세 커리큘럼 명세서)

> "코드 한 줄부터 시작해 쿠버네티스 프로덕션 클러스터와 드리프트 모니터링까지"  
> 총 7개 Phase, 20개 강의로 구성된 MLOps 풀스택 실무 커리큘럼입니다.

---

## 🟢 Phase 1: MLOps 엔지니어링 기초 (기반 다지기)

### [제1강] MLOps 풀스택 개발 환경 구축 및 Git/GitHub 마스터
- **목표**: MLOps의 큰 그림을 이해하고, 격리된 파이썬 가상환경 및 Git 버전 관리 실무 체계를 확립한다.
- **핵심 키워드**: `venv`, `pip`, `.gitignore`, `GitLens`, `CUDA/GPU Check`, `Reproducibility`
- **이론**:
  - 데이터 과학자(Jupyter) vs 백엔드 엔지니어 vs MLOps 엔지니어의 차이
  - 파이썬 인터프리터 작동 원리와 패키지 격리(`venv`, `uv`, `conda` 비교)
  - MLOps 프로젝트에서 `.gitignore`가 생명인 이유 (대용량 모델 가중치, 데이터 유출 방지)
- **실습**:
  - VS Code 최적 설정 (`settings.json`, `extensions.json`)
  - Python 가상환경 생성 및 활성화 스크립트
  - 하드웨어(CPU/RAM/GPU), OS, 파이썬 환경을 자동 진단하는 `check_env.py` 작성 및 실행
  - GitHub 첫 커밋 & 푸시
- **산출물**: `01_environment_and_git/scripts/check_env.py`, `system_diagnostic_report.md`

### [제2강] 모던 파이썬 & 객체지향 설계(OOP) 및 Pydantic 데이터 검증
- **목표**: MLOps 코드베이스에 필요한 파이썬 클린 코드, 타입 힌팅, Pydantic 데이터 모델링을 체화한다.
- **핵심 키워드**: `Type Hints`, `Pydantic v2`, `Dataclass`, `OOP Design Pattern`, `Factory Pattern`
- **실습**:
  - 모델 설정(Config) 관리 클래스 설계
  - Pydantic을 이용한 머신러닝 입력 데이터 유효성 검증(Validation) 파이프라인

### [제3강] 터미널과 쉘 스크립트 실무 (PowerShell, Bash, WSL2)
- **목표**: 리눅스 기반 컨테이너와 서버 환경을 다루기 위한 쉘 스크립팅 능력을 배양한다.
- **핵심 키워드**: `PowerShell`, `Bash Scripting`, `Environment Variables`, `WSL2`, `Path & Exit Code`
- **실습**: 자동 환경 구성 및 파이프라인 원클릭 실행 스크립트(`run.sh`, `run.ps1`) 제작

---

## 🟡 Phase 2: 머신러닝 & 딥러닝 핵심 파이프라인

### [제4강] 프로덕션 데이터 파이프라인 (Pandas & Polars, 데이터 품질 검증)
- **목표**: 단순 탐색용 EDA를 넘어 배포 가능한 재현성 있는 데이터 전처리 파이프라인을 구축한다.
- **핵심 키워드**: `Polars`, `Pandas`, `Great Expectations`, `Data Drift Premise`, `Missing Values`

### [제5강] Scikit-Learn 머신러닝 실전 파이프라인
- **목표**: 모델과 전처리가 하나로 묶인 누수(Data Leakage) 없는 `sklearn.pipeline.Pipeline` 구현.
- **핵심 키워드**: `ColumnTransformer`, `StandardScaler`, `Pipeline`, `Joblib`, `Model Serialization`

### [제6강] PyTorch 딥러닝 코어 파이프라인
- **목표**: PyTorch로 모듈화된 학습/검증 루프와 GPU 가속 파이프라인을 작성한다.
- **핵심 키워드**: `Dataset`, `DataLoader`, `nn.Module`, `Device Agnostic Code (CPU/CUDA/MPS)`, `Checkpointing`

---

## 🟠 Phase 3: 백엔드 API & 모델 서빙 (Serving & Backend)

### [제7강] FastAPI 기반 초고속 REST API 구축
- **목표**: 파이썬 최고의 비동기 웹 프레임워크인 FastAPI로 머신러닝 예측 API를 설계한다.
- **핵심 키워드**: `FastAPI`, `ASGI (Uvicorn)`, `Pydantic Request/Response`, `Async/Await`, `Dependency Injection`

### [제8강] 프로덕션 머신러닝 서빙 아키텍처
- **목표**: 지연 시간(Latency) 최소화와 대용량 트래픽에 대응하는 서빙 최적화 기법을 적용한다.
- **핵심 키워드**: `Lifespan Events (In-Memory Model Loading)`, `Batch Inference`, `ONNX Runtime`, `Concurrency`

### [제9강] Docker 컨테이너화 (Packaging & Isolation)
- **목표**: 머신러닝 서빙 애플리케이션을 어디서나 동일하게 동작하도록 도커 이미지로 패키징한다.
- **핵심 키워드**: `Dockerfile`, `Multi-Stage Build`, `Slim/Alpine vs Debian`, `.dockerignore`, `Port Binding`

---

## 🔵 Phase 4: 프론트엔드 & 인터랙티브 대시보드 (Full-Stack UI)

### [제10강] Streamlit & Gradio를 활용한 인터랙티브 데모 UI
- **목표**: 비개발자/사용자가 모델의 결과를 즉시 테스트할 수 있는 웹 UI를 고속으로 제작한다.
- **핵심 키워드**: `Streamlit State`, `File Uploader`, `Real-Time Plotting`, `Gradio Interface`

### [제11강] 모던 웹 프론트엔드 연동 기초
- **목표**: 백엔드 FastAPI와 직접 통신하는 웹 프론트엔드(React/Next.js 또는 모던 JS)를 구현한다.
- **핵심 키워드**: `Fetch API`, `CORS`, `JSON Payload`, `UI State Management`, `Responsive Design`

### [제12강] 실시간 모델 제어 및 시각화 대시보드
- **목표**: 예측 히스토리, 모델 신뢰도, 입력 데이터 분포를 한눈에 볼 수 있는 풀스택 대시보드를 완성한다.

---

## 🟣 Phase 5: MLOps 핵심 생태계 (실험 추적 & 버전 관리)

### [제13강] MLflow를 활용한 실험 추적 (Experiment Tracking)
- **목표**: 모델 하이퍼파라미터, 메트릭, 아티팩트를 중앙 서버에 기록하고 비교 분석한다.
- **핵심 키워드**: `MLflow Tracking`, `Autologging`, `Runs & Experiments`, `Artifacts Storage`

### [제14강] DVC를 활용한 데이터 & 모델 버전 관리
- **목표**: 코드(Git)와 데이터/모델(DVC)의 버전을 1:1로 동기화한다.
- **핵심 키워드**: `DVC Remote (S3 / Local Storage)`, `dvc.yaml`, `Data Lineage`, `Reproducibility`

### [제15강] Model Registry와 모델 수명주기 관리
- **목표**: 모델의 개발 -> 스테이징 -> 프로덕션 전환을 시스템적으로 관리한다.
- **핵심 키워드**: `MLflow Model Registry`, `Model Versioning`, `Model Aliases`, `Production Promotion`

---

## 🟤 Phase 6: 파이프라인 자동화 & CI/CD

### [제16강] GitHub Actions를 이용한 MLOps CI/CD
- **목표**: Git 푸시 시 자동으로 코드 품질 검사, 모델 테스트, 도커 빌드/푸시를 수행한다.
- **핵심 키워드**: `GitHub Actions`, `CI/CD Workflows`, `pytest`, `Ruff/Black`, `Docker Hub Registry`

### [제17강] 파이프라인 오케스트레이션 (Prefect / Airflow)
- **목표**: 정기적인 데이터 수집, 모델 재학습, 검증 파이프라인을 자동 스케줄링한다.
- **핵심 키워드**: `DAG (Directed Acyclic Graph)`, `Prefect Flow & Task`, `Retry Policy`, `Failure Notification`

---

## 🔴 Phase 7: 프로덕션 배포 & 관측성 (Final Boss)

### [제18강] 클라우드 배포 기초 & Kubernetes(K8s) 모델 서빙
- **목표**: 컨테이너화된 모델을 클라우드 및 쿠버네티스 클러스터에 배포하여 오토스케일링을 구현한다.
- **핵심 키워드**: `K8s Pod / Deployment / Service`, `HPA (Horizontal Pod Autoscaler)`, `Ingress`, `Rolling Update`

### [제19강] 모델 성능 저하 & 데이터 드리프트 실시간 모니터링
- **목표**: 서비스 중인 모델의 성능 변화 및 데이터 분포 변화(Drift)를 실시간으로 감지한다.
- **핵심 키워드**: `Data Drift`, `Concept Drift`, `Evidently AI`, `Prometheus Metrics`, `Grafana Dashboard`

### [제20강] 최종 실전 풀스택 캡스톤 프로젝트
- **목표**: 데이터 수집부터 웹 UI, API, 모니터링, 자동 재학습까지 결합된 완성형 AI 프로덕트 완성.
- **핵심 키워드**: `End-to-End System`, `Portfolio Packaging`, `Live Production Ready`
