# [MLOps Full-Stack 04강] run_pipeline.ps1
# Windows PowerShell 환경 MLOps 원클릭 자동화 스크립트
# 사용법:
#   .\run_pipeline.ps1
#   .\run_pipeline.ps1 -Stage production
#   .\run_pipeline.ps1 -TriggerError

param(
    [string]$Stage = "development",
    [switch]$TriggerError
)

# 콘솔 인코딩을 UTF-8로 설정
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "🚀 [MLOps 04강] PowerShell 원클릭 파이프라인 시작" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. 실행 인자 및 환경 변수 주입
Write-Host "[1/4] 환경 변수 설정 중... (Stage: $Stage)" -ForegroundColor Yellow
$env:STAGE = $Stage
$env:SECRET_KEY = "dummy-mlops-token-12345"

# 2. 작업 디렉토리 설정 및 로그 디렉토리 생성
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Resolve-Path "$ScriptDir\..\.."
$LogDir = "$ScriptDir\..\logs"

if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir | Out-Null
}
$LogFile = "$LogDir\pipeline_run_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"

Write-Host "[2/4] 로그 저장 경로: $LogFile" -ForegroundColor Yellow

# 3. 파이썬 스크립트 실행
Write-Host "[3/4] 파이썬 파이프라인 실행 중..." -ForegroundColor Yellow

$PythonScript = "$ScriptDir\test_target.py"
$PythonArgs = @("--mode", "automated_run")

if ($TriggerError) {
    $PythonArgs += "--fail"
}

# 파이썬 실행 및 콘솔 & 로그 파일 동시 기록
python $PythonScript $PythonArgs *>&1 | Tee-Object -FilePath $LogFile

# 4. 종료 코드(Exit Code) 확인 ($LASTEXITCODE)
$ExitCode = $LASTEXITCODE

Write-Host "`n[4/4] 파이프라인 실행 결과 검증..." -ForegroundColor Yellow
if ($ExitCode -eq 0) {
    Write-Host "==========================================================" -ForegroundColor Green
    Write-Host "✅ 파이프라인 정상 종료 (Exit Code: $ExitCode)" -ForegroundColor Green
    Write-Host "==========================================================" -ForegroundColor Green
} else {
    Write-Host "==========================================================" -ForegroundColor Red
    Write-Host "❌ 파이프라인 비정상 실패! (Exit Code: $ExitCode)" -ForegroundColor Red
    Write-Host "   상세 에러 내역은 로그 파일을 확인하세요: $LogFile" -ForegroundColor Red
    Write-Host "==========================================================" -ForegroundColor Red
}

# 최종 종료 코드를 상위 프로세스로 전파
exit $ExitCode
