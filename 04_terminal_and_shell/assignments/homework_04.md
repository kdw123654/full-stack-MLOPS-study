# 📝 [제4강 과제] MLOps 서버 헬스체크 & 로그 백업 자동화 스크립트 제작

축하합니다! 4강에서는 MLOps 엔지니어의 핵심 무기인 **터미널 명령어, PowerShell/Bash 스크립팅, 환경 변수, 그리고 종료 코드(Exit Code)**를 배웠습니다.  
이번 과제는 배운 내용을 바탕으로 **내 서버 환경의 파이썬, 디스크 용량, 로그 상태를 한 번에 점검하는 헬스체크 스크립트**를 직접 완성하는 실습 미션입니다.

---

## 🎯 과제 목표
Windows PowerShell 스크립트인 `health_check.ps1`을 작성하여 다음 4가지 검사를 자동으로 수행하고 보고서를 생성하세요.

### 📋 세부 요구 조건
1. **스크립트 파일명**: `assignments/health_check.ps1`
2. **검사 항목**:
   - **Step 1: Python 확인**: 현재 실행 가능한 `python --version`을 호출하고 버전을 변수에 저장
   - **Step 2: 환경 변수 점검**: `$env:STAGE`가 설정되어 있는지 확인 (미설정이면 "development"로 기본값 부여)
   - **Step 3: 로그 디렉토리 점검**: `04_terminal_and_shell/logs` 폴더가 존재하는지 확인하고, 내부 로그 파일 개수를 카운트
   - **Step 4: 리포트 파일 생성**: 위 검사 결과들을 `04_terminal_and_shell/logs/health_report.txt`에 저장
3. **종료 코드 반환**: 모든 작업이 성공하면 `exit 0` 반환

---

## 💻 실습 코드 템플릿 (`assignments/health_check.ps1`)

```powershell
# [제4강 과제] health_check.ps1
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "[HEALTH-CHECK] MLOps 서버 헬스체크 스크립트 가동" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

# 1. Python 버전 확인
$pyVersion = python --version 2>&1
Write-Host "1. Python 버전: $pyVersion" -ForegroundColor Green

# 2. 환경 변수 확인 및 기본값 처리
$currentStage = if ($env:STAGE) { $env:STAGE } else { "development (기본값)" }
Write-Host "2. 배포 스테이지: $currentStage" -ForegroundColor Green

# 3. 로그 디렉토리 확인 및 파일 개수 카운트
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$logDir = "$scriptDir\..\logs"

if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir | Out-Null
}

$logCount = (Get-ChildItem -Path $logDir -Filter "*.log").Count
Write-Host "3. 보관 중인 로그 파일 수: $logCount 개" -ForegroundColor Green

# 4. 리포트 파일 저장
$reportFile = "$logDir\health_report.txt"
$reportLines = @(
    "=============================================",
    "[REPORT] MLOps 시스템 헬스체크 보고서",
    "생성 시각: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')",
    "=============================================",
    "- Python 버전: $pyVersion",
    "- 환경(Stage): $currentStage",
    "- 로그 파일 수: $logCount 개",
    "- 시스템 상태: NORMAL (정상)",
    "============================================="
)

$reportLines | Out-File -FilePath $reportFile -Encoding UTF8
Write-Host ""
Write-Host "[SUCCESS] 헬스체크 완료! 보고서가 저장되었습니다: $reportFile" -ForegroundColor Cyan

exit 0
```

---

## 🚀 과제 실행 및 Git 커밋

VS Code 터미널에서 아래 명령어로 스크립트를 실행해 보세요:

```powershell
# 1. 스크립트 실행
.\04_terminal_and_shell\assignments\health_check.ps1

# 2. 생성된 리포트 내용 터미널에서 확인
cat .\04_terminal_and_shell\logs\health_report.txt
```

성공적으로 실행되었다면 변경사항을 GitHub에 커밋하고 푸시합니다:

```powershell
git status
git add .
git commit -m "feat: complete lesson 04 terminal and shell scripting"
git push origin main
```

모두 완료하셨다면 Phase 1 (MLOps 엔지니어링 기초 1~4강)을 완벽하게 졸업하신 것입니다! 🎉
