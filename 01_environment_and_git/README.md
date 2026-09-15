# 📖 [제1강] MLOps 풀스택 개발 환경 구축 및 Git/GitHub 실무 마스터

> **"모든 위대한 AI 서비스는 재현 가능한(Reproducible) 깨끗한 개발 환경과 철저한 버전 관리에서 시작됩니다."**

---

## 🎯 이번 강의 학습 목표
1. **MLOps 풀스택의 정의와 역할**을 이해하고, 단순 모델러와의 차이점을 명확히 인식한다.
2. **VS Code**를 파이썬 풀스택 및 MLOps 개발에 최적화된 상태로 세팅한다.
3. 파이썬 인터프리터의 패키지 탐색 원리와 **가상환경(`venv`) 격리의 절대적인 필요성**을 배운다.
4. MLOps 프로젝트 관점에서 **`.gitignore`의 보안/용량 원칙**을 배우고, **Git/GitHub 실무 워크플로우**를 익힌다.
5. 시스템 사양, 파이썬 환경, GPU(CUDA) 가속 상태를 점검하는 **환경 진단 자동화 스크립트(`check_env.py`)**를 작성 및 실행한다.

---

## 1. MLOps 풀스택이란 무엇인가?

### 1.1 데이터 과학자 vs 백엔드 엔지니어 vs MLOps 풀스택
많은 분들이 머신러닝/딥러닝을 배울 때 `Jupyter Notebook (.ipynb)`에서 데이터를 불러오고, `model.fit()`을 돌려 정확도(Accuracy) 95%가 나오면 끝난다고 생각합니다. 하지만 이는 전체 AI 프로덕트의 **10%**에 불과합니다.

```
┌────────────────────────────────────────────────────────┐
│               전체 AI 서비스 생태계                   │
│                                                        │
│  [데이터 수집/검증] ──► [ML/DL 모델링] ──► [API 서빙]   │
│           │                     │               │      │
│           ▼                     ▼               ▼      │
│     (DVC, Polars)         (PyTorch)         (FastAPI)  │
│                                                 │      │
│  [모니터링 & 재학습] ◄── [CI/CD & 배포] ◄── [사용자 UI]│
│  (Evidently, Grafana)   (GitHub, Docker)   (Streamlit) │
└────────────────────────────────────────────────────────┘
```

- **전통적인 데이터 과학자**: 노트북 안에서 최적의 알고리즘과 하이퍼파라미터를 찾아 모델을 만듭니다. (운영 및 서비스화 경험 부족)
- **전통적인 백엔드 엔지니어**: 웹 서버, 데이터베이스, 트래픽 분산에는 능숙하지만 모델의 특성(GPU 메모리 점유, 배치 추론, 데이터 드리프트)을 모릅니다.
- **MLOps 풀스택 엔지니어 (우리의 목표)**:
  - 사용자가 접근할 수 있는 **웹 UI (프론트엔드)**를 이해하고 연결합니다.
  - 모델을 실시간으로 서빙하는 **고성능 REST API (FastAPI)**를 구축합니다.
  - 최신 **딥러닝 모델 (PyTorch)**을 학습 및 경량화합니다.
  - 코드와 데이터, 모델을 통제하고 자동 배포하는 **MLOps 파이프라인 (Docker, CI/CD, MLflow)**을 운영합니다.

---

## 2. VS Code 개발 환경 최적화 (Windows 기준)

VS Code는 현재 전 세계에서 가장 널리 쓰이는 가볍고 확장성이 뛰어난 IDE입니다. MLOps 풀스택 개발자는 다음 세팅을 갖추어야 합니다.

### 2.1 필수 Extension (확장 프로그램)
VS Code의 확장 탭(`Ctrl + Shift + X`)에서 다음 확장들을 반드시 설치해 주세요. (레포지토리의 `.vscode/extensions.json`에 이미 등록되어 있어 권장 알림이 뜹니다.)

1. **Python (Microsoft)**: 파이썬 코드 실행, 디버깅, IntelliSense 제공
2. **Pylance (Microsoft)**: 정적 타입 검사 및 초고속 코드 자동완성
3. **Ruff (Astral Software)**: 실무 표준 초고속 Python 린터(Linter) 및 코드 포맷터(Formatter)
4. **GitLens (GitKraken)**: 코드 라인별 커밋 작성자 확인, 브랜치 비교, 히스토리 탐색
5. **Docker (Microsoft)**: 도커 컨테이너, 이미지 관리 및 Dockerfile 구문 지원
6. **Even Better TOML / YAML**: 설정 파일(`pyproject.toml`, Docker Compose, K8s yaml) 가독성 향상
7. **Jupyter (Microsoft)**: VS Code 내부에서 바로 `.ipynb` 노트북을 열고 디버깅

### 2.2 VS Code 작업 영역 설정 (`.vscode/settings.json`)
파일을 저장할 때마다 자동으로 코드를 규격에 맞게 정렬(Auto-formatting)하고 사용하지 않는 `import` 구문을 정리하도록 설정합니다:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
  "python.analysis.typeCheckingMode": "basic",
  "python.analysis.autoImportCompletions": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": "explicit"
  },
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true
  }
}
```

---

## 3. Python 가상환경(Virtual Environment)의 본질

### 3.1 "제 컴퓨터에선 잘 돌아가는데요?"의 비극
파이썬 초보자가 가장 많이 겪는 참사는 **글로벌 파이썬(시스템 기본 파이썬)** 환경에 모든 라이브러리를 무작정 `pip install` 하는 것입니다.
- 프로젝트 A는 `numpy==1.24.0`이 필요한데, 프로젝트 B를 하며 `numpy==2.0.0`을 깔면 기존 프로젝트 A가 먹통이 됩니다.
- 특히 PyTorch는 CUDA 버전과 일치해야 하는데, 글로벌에 꼬이면 삭제 후 재설치조차 복잡해집니다.

### 3.2 `venv`의 동작 원리
가상환경은 거창한 가상머신이 아닙니다. **특정 폴더 안에 파이썬 실행 파일(`python.exe`)의 복사본(심볼릭 링크)과 독립된 패키지 저장소(`Lib/site-packages`)를 만드는 것**입니다.

```
내 프로젝트 폴더/
├── .venv/                      <-- 독립된 가상환경 폴더
│   ├── Scripts/
│   │   ├── python.exe          <-- 이 프로젝트 전용 파이썬
│   │   ├── pip.exe
│   │   └── Activate.ps1        <-- 가상환경 켜는 스크립트
│   └── Lib/
│       └── site-packages/      <-- 여기에 설치된 패키지만 사용!
```

### 3.3 가상환경 명령어 (PowerShell 기준 실습)

#### 1) 가상환경 생성하기
프로젝트 루트 경로(`mlops full-stack`) 터미널에서 다음을 입력합니다:
```powershell
python -m venv .venv
```
> 💡 폴더 이름을 `.venv`로 지정하면 VS Code가 자동으로 인식하며, Git에서도 숨김 처리하기 좋습니다.

#### 2) 가상환경 활성화(Activate)하기
```powershell
.venv\Scripts\Activate.ps1
```
활성화되면 터미널 프롬프트 앞에 `(.venv)`라는 표시가 붙습니다:
```powershell
(.venv) PS C:\Users\kimk1\OneDrive\Desktop\mlops full-stack>
```

#### 3) 가상환경 비활성화(Deactivate)
작업을 마쳤거나 가상환경을 벗어날 때는:
```powershell
deactivate
```

---

## 4. Git & GitHub 실무 워크플로우

### 4.1 MLOps에서 `.gitignore`가 생명선인 이유
웹 개발과 달리, MLOps 프로젝트에는 **거대한 데이터셋(GB 단위의 CSV, 이미지 등)**과 **딥러닝 모델 가중치 파일(`.pt`, `.bin`, `.onnx`)**이 존재합니다.
- GitHub는 **단일 파일 100MB 초과 시 푸시를 차단(Reject)**합니다. 실수로 커밋하고 푸시하려 하면 커밋 히스토리 전체가 오염되어 복구하기 매우 까다롭습니다.
- `.env` 파일에 작성된 클라우드 API 키(OpenAI 키, AWS 시크릿 키)가 실수로 GitHub에 퍼블릭으로 올라가면 수 분 내에 수백~수천만 원의 과금이 발생할 수 있습니다.
- 따라서 프로젝트 시작 전 반드시 철저한 `.gitignore`를 등록해야 합니다.

### 4.2 필수 제외 항목들 (본 레포지토리에 적용된 내용)
- 가상환경 폴더: `.venv/`, `venv/`
- 파이썬 캐시: `__pycache__/`, `*.pyc`
- 모델 가중치: `*.pt`, `*.pth`, `*.onnx`, `*.pkl` (추후 DVC로 별도 관리)
- 대용량 데이터: `data/raw/*`
- 시크릿: `.env`, `*.key`, `*.pem`

### 4.3 Git 실무 워크플로우 4단계
```powershell
# 1단계: 변경된 파일 상태 확인
git status

# 2단계: 커밋할 파일 스테이징에 올리기
git add .

# 3단계: 의미 있는 커밋 메시지와 함께 기록
git commit -m "feat: complete lesson 01 environment setup and check_env script"

# 4단계: GitHub 원격 저장소에 업로드
git push origin main
```

---

## 5. 실습: 나만의 개발 환경 진단 도구 `check_env.py`

본 1강에는 학습자의 현재 컴퓨터 하드웨어(CPU, RAM, GPU), 운영체제, 파이썬 버전, 가상환경 적용 여부, Git 저장소 상태를 자동으로 진단하고 Markdown 리포트를 뽑아내는 전문 진단 스크립트가 준비되어 있습니다.

### 5.1 실습 단계

#### STEP 1: 가상환경이 켜져 있는지 확인 (`(.venv)`)
터미널에서 가상환경이 켜져 있지 않다면 켜줍니다:
```powershell
.venv\Scripts\Activate.ps1
```

#### STEP 2: 1강 필수 패키지 설치
```powershell
cd 01_environment_and_git
pip install -r requirements.txt
```

#### STEP 3: 환경 진단 스크립트 실행
```powershell
python scripts/check_env.py
```

#### STEP 4: 결과 확인
터미널에 컬러 표로 결과가 출력되며, 자동으로 `01_environment_and_git/system_diagnostic_report.md` 파일이 생성됩니다!

---

## 6. 트러블슈팅 & FAQ

### Q1. PowerShell에서 `.venv\Scripts\Activate.ps1`을 실행하려는데 `이 시스템에서 스크립트를 실행할 수 없으므로...` 오류가 뜹니다!
**원인**: Windows PowerShell의 기본 보안 정책(ExecutionPolicy)이 외부 스크립트 실행을 제한(`Restricted`)하기 때문입니다.  
**해결법**: 현재 터미널 세션에 한해 권한을 일시 허용해 줍니다:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.venv\Scripts\Activate.ps1
```
*(또는 PowerShell을 관리자 권한으로 열어 `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`를 실행해도 됩니다.)*

### Q2. `nvidia-smi`를 치면 그래픽카드가 보이는데, PyTorch에서는 GPU가 안 잡힙니다!
**원인**: PyTorch를 일반 `pip install torch`로 설치하면 기본적으로 **CPU 전용 휠(Wheel)**이 다운로드되기 때문입니다.  
**해결법**: 본인의 CUDA 버전에 맞는 공식 명령어로 설치해야 합니다. (우리는 6강 PyTorch 딥러닝 편에서 CUDA 버전에 맞춰 정확히 설치할 예정이니 지금은 걱정하지 않으셔도 됩니다!)

### Q3. VS Code 터미널을 열었을 때 자동으로 가상환경이 안 켜져요.
**해결법**:
1. VS Code에서 `Ctrl + Shift + P`를 누릅니다.
2. `Python: Select Interpreter`를 입력하고 선택합니다.
3. 목록에서 `('.venv': venv) .\.venv\Scripts\python.exe`를 클릭합니다.
4. 이후 새 터미널(`Ctrl + ~`)을 열면 자동으로 가상환경이 켜집니다.

---

## 7. 제1강 실습 과제
이론과 실습을 마쳤다면, [1강 과제 가이드](assignments/homework_01.md)를 열고 첫 번째 스터디 미션을 완료해 보세요!  
과제를 완료하고 커밋을 남기면, 여러분의 GitHub 스터디 레포지토리가 멋진 기술 블로그이자 포트폴리오의 첫 페이지로 완성됩니다.
