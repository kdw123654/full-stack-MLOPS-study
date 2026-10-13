# 📖 [제4강] 터미널과 쉘 스크립트 실무 (PowerShell, Bash, WSL2 & 자동화)

> **"프로덕션 서버와 클라우드 컨테이너에는 모니터와 마우스가 없습니다.  
> MLOps 엔지니어의 진정한 무기는 검은 터미널 화면과 몇 줄의 강력한 쉘 스크립트입니다."**

---

## 🎯 이번 강의 학습 목표
1. **CLI(Command Line Interface)**의 동작 원리를 이해하고, 왜 MLOps 파이프라인에서 GUI(마우스 클릭) 대신 터미널이 필수적인지 깨닫는다.
2. Windows의 **PowerShell**과 Linux/macOS/Docker의 표준인 **Bash**의 핵심 명령어를 1:1로 비교하고 자유자재로 다룬다.
3. 보안 토큰, 스테이징 환경, API 설정을 분리하는 **환경 변수(Environment Variables)**를 다루고 파이썬과 연동한다.
4. 모든 자동화의 기본 원리인 **종료 코드(Exit Code)**와 파이프(`|`), 리다이렉션(`>`, `>>`)을 마스터한다.
5. 복잡한 파이썬 실행, 인자 전달, 환경 변수 주입, 로그 저장을 한 번에 처리하는 **원클릭 쉘 자동화 스크립트(`run_pipeline.ps1`, `run_pipeline.sh`)**를 구축한다.

---

## 1. 왜 MLOps 엔지니어에게 터미널과 쉘 스크립트가 필수인가?

### 1.1 "서버에는 모니터가 없다 (Headless 환경)"
우리가 7강부터 만들 백엔드 API, 9강의 Docker 컨테이너, 16강의 GitHub Actions 자동화, 18강의 Kubernetes 클라우드 클러스터는 **모두 리눅스 터미널(CLI) 환경**에서 동작합니다.
- 마우스로 클릭해서 모델을 돌릴 수 없습니다.
- "매일 새벽 2시에 데이터를 수집하고 모델을 학습시킨 뒤 서버를 재시작하라"는 명령은 **쉘 스크립트(.sh 또는 .ps1)**로 작성되어 서버 백그라운드에서 돌아갑니다.

```
[ 개발자 PC (Windows VS Code) ] 
       │ 
       ▼ (Git Push)
[ GitHub Actions CI/CD (Ubuntu Linux) ] ──► (쉘 스크립트로 테스트 자동 실행)
       │
       ▼ (Docker Build)
[ 클라우드 서버 / Kubernetes (Linux 컨테이너) ] ──► (쉘 스크립트로 모델 서빙 가동)
```

---

## 2. Windows(PowerShell) vs Linux(Bash) 명령어 완벽 치트시트

Windows 사용자가 Linux 기반 MLOps 환경(Docker, 클라우드)에 쉽게 적응할 수 있도록 가장 많이 쓰이는 필수 명령어를 정리했습니다:

| 작업 내용 | Linux / macOS / Bash | Windows PowerShell | 설명 |
| :--- | :--- | :--- | :--- |
| **현재 경로 확인** | `pwd` | `pwd` (또는 `Get-Location`) | Print Working Directory |
| **파일/폴더 목록** | `ls -la` | `ls` (또는 `Get-ChildItem`) | 숨김 파일 및 상세 정보 포함 |
| **폴더 이동** | `cd 폴더명` | `cd 폴더명` | 상위 폴더는 `cd ..` |
| **폴더 생성** | `mkdir data` | `mkdir data` (또는 `New-Item`) | Make Directory |
| **파일 내용 출력** | `cat file.txt` | `cat file.txt` (또는 `Get-Content`) | 파일 내용 터미널에 보기 |
| **파일/폴더 강제 삭제** | `rm -rf data` | `Remove-Item -Recurse -Force data` | ⚠️ 주의해서 사용 |
| **텍스트 검색** | `grep "ERROR" app.log` | `Select-String "ERROR" app.log` | 로그에서 특정 단어 찾기 |
| **네트워크 HTTP 요청**| `curl -X GET http://...`| `curl` (또는 `Invoke-RestMethod`) | API 통신 테스트 |
| **프로세스 확인/종료**| `ps aux \| grep python`<br>`kill -9 <PID>` | `Get-Process python`<br>`Stop-Process -Id <PID>` | 먹통 된 파이썬 강제 종료 |

---

## 3. MLOps의 핵심 방패: 환경 변수 (Environment Variables)

### 3.1 환경 변수란?
운영체제(OS)가 메모리에 띄워두고 있는 **전역 딕셔너리(Key-Value)**입니다.  
프로그램이 실행될 때 OS로부터 이 딕셔너리를 전달받아 참조합니다.

### 3.2 왜 환경 변수를 써야 하는가? (코드에 하드코딩 금지!)
```python
# ❌ 절대 안 되는 나쁜 예 (깃허브에 올라가면 수천만 원 과금 발생!)
OPENAI_API_KEY = "sk-proj-1234567890abcdef"
DB_PASSWORD = "my-secret-password"

# ✅ 올바른 실무 예 (환경 변수에서 안전하게 읽어오기)
import os
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
STAGE = os.environ.get("STAGE", "development") # 기본값 지정
```

### 3.3 터미널에서 환경 변수 다루기

#### Windows PowerShell:
```powershell
# 환경 변수 설정
$env:STAGE = "production"
$env:MY_SECRET = "super_secure_key"

# 환경 변수 확인
echo $env:STAGE

# 환경 변수 삭제
Remove-Item env:STAGE
```

#### Linux / Bash:
```bash
# 환경 변수 설정 (export 필수!)
export STAGE="production"
export MY_SECRET="super_secure_key"

# 환경 변수 확인
echo $STAGE

# 환경 변수 해제
unset STAGE
```

---

## 4. 종료 코드(Exit Code)와 파이프라인 제어

컴퓨터의 모든 프로그램(파이썬, Git, 도커 등)은 실행이 끝나면 OS에게 **숫자 하나(종료 코드)**를 남기고 죽습니다.

- **`0`**: "성공적으로 잘 끝났습니다! (Success)"
- **`0이 아닌 숫자 (1, 2, 137, 255 등)`**: "에러가 발생했습니다! (Failure)"

### 4.1 직전 명령어 성공 여부 확인
- **PowerShell**: `$LASTEXITCODE`
- **Bash**: `$?`

### 4.2 연쇄 실행 연산자
- **`&&` (AND)**: 앞의 명령어가 성공(0)했을 때만 뒤의 명령어 실행
  ```powershell
  # 테스트가 통과해야만 배포 스크립트 실행
  pytest && python deploy.py
  ```
- **`||` (OR)**: 앞의 명령어가 실패했을 때 대안 명령어 실행
  ```powershell
  python check_gpu.py || echo "GPU가 없어 CPU 모드로 전환합니다."
  ```

### 4.3 리다이렉션(`>`, `>>`)과 파이프(`|`)
- `>` : 출력 결과를 파일로 저장 (덮어쓰기)
- `>>`: 출력 결과를 파일 끝에 이어 붙이기 (Append)
- `|` (파이프): 앞 프로그램의 출력을 뒷 프로그램의 입력으로 즉시 전달 (예: `python train.py | tee train.log`)

---

## 5. 실습: 원클릭 MLOps 자동화 스크립트

본 강의에는 환경 변수 주입, 파이썬 실행, 로그 파일 자동 저장, 종료 코드 검증을 완벽하게 처리하는 실전 스크립트가 준비되어 있습니다.

### 5.1 PowerShell 스크립트 실행 실습 (Windows)

#### 1) 정상 실행 테스트
```powershell
# 04_terminal_and_shell 폴더에서 실행
cd 04_terminal_and_shell
.\scripts\run_pipeline.ps1 -Stage production
```
- 화면에 초록색으로 `✅ 파이프라인 정상 종료 (Exit Code: 0)`가 뜨는지 확인합니다.
- `logs/` 폴더 아래에 타임스탬프가 찍힌 로그 파일(`pipeline_run_YYYYMMDD_HHMMSS.log`)이 잘 생성되었는지 확인합니다.

#### 2) 에러 발생 및 감지 테스트
```powershell
.\scripts\run_pipeline.ps1 -TriggerError
```
- 화면에 빨간색으로 `❌ 파이프라인 비정상 실패! (Exit Code: 1)`가 뜨며 스크립트가 에러를 정확히 감지하는지 확인합니다.

---

## 6. 트러블슈팅 & FAQ

### Q1. PowerShell에서 스크립트를 실행하려는데 권한 오류(`Execution_Policies`)가 떠요!
**원인**: Windows는 악성 스크립트 방지를 위해 기본적으로 외부 `.ps1` 실행을 막습니다.  
**해결법**: 현재 VS Code 터미널 세션에 권한을 부여합니다:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

### Q2. 윈도우에서 만든 `.sh` 스크립트를 리눅스/도커에서 돌렸더니 `\r: command not found` 에러가 나요!
**원인**: 줄바꿈 문자 차이입니다. Windows는 `CRLF(\r\n)`, Linux는 `LF(\n)`를 씁니다.  
**해결법**: VS Code 우측 하단 상태표시줄에서 `CRLF`를 클릭하여 `LF`로 변경 후 저장합니다.

---

## 7. 제4강 실습 과제
이론과 실습을 마쳤다면, [4강 과제 가이드](assignments/homework_04.md)를 열어 나만의 시스템 헬스체크 & 로그 백업 자동화 스크립트를 작성해 보세요!
