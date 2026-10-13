# [제4강 과제 정답] solution_04.ps1
# MLOps 서버 헬스체크 및 로그 분석 자동화 스크립트

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
