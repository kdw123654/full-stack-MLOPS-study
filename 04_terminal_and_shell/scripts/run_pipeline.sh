#!/usr/bin/env bash
# [MLOps Full-Stack 04강] run_pipeline.sh
# Linux / macOS / WSL2 / Docker / CI-CD 환경용 Bash 쉘 스크립트
# 사용법:
#   ./run_pipeline.sh
#   ./run_pipeline.sh production
#   ./run_pipeline.sh production --fail

# 에러 발생 시 즉시 중단 및 파이프 에러 추적
set -eo pipefail

STAGE="${1:-development}"
TRIGGER_FAIL="${2:-}"

echo "=========================================================="
echo "🚀 [MLOps 04강] Linux/Bash 원클릭 파이프라인 시작"
echo "=========================================================="

# 1. 환경 변수 주입
echo "[1/4] 환경 변수 설정 중... (STAGE: ${STAGE})"
export STAGE="${STAGE}"
export SECRET_KEY="dummy-mlops-token-12345"

# 2. 경로 및 로그 디렉토리 준비
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="${SCRIPT_DIR}/../logs"
mkdir -p "${LOG_DIR}"
LOG_FILE="${LOG_DIR}/pipeline_run_$(date +'%Y%m%d_%H%M%S').log"

echo "[2/4] 로그 저장 경로: ${LOG_FILE}"

# 3. 파이썬 스크립트 실행
echo "[3/4] 파이썬 파이프라인 실행 중..."
PYTHON_SCRIPT="${SCRIPT_DIR}/test_target.py"
PYTHON_ARGS=("--mode" "automated_run")

if [ "${TRIGGER_FAIL}" == "--fail" ]; then
    PYTHON_ARGS+=("--fail")
fi

python "${PYTHON_SCRIPT}" "${PYTHON_ARGS[@]}" 2>&1 | tee "${LOG_FILE}"
EXIT_CODE="${PIPESTATUS[0]}"

# 4. 종료 코드 확인
echo ""
echo "[4/4] 파이프라인 실행 결과 검증..."
if [ "${EXIT_CODE}" -eq 0 ]; then
    echo "=========================================================="
    echo "✅ 파이프라인 정상 종료 (Exit Code: ${EXIT_CODE})"
    echo "=========================================================="
else
    echo "=========================================================="
    echo "❌ 파이프라인 비정상 실패! (Exit Code: ${EXIT_CODE})"
    echo "   로그 파일을 확인하세요: ${LOG_FILE}"
    echo "=========================================================="
fi

exit "${EXIT_CODE}"
