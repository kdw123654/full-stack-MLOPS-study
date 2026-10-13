"""
[MLOps Full-Stack 04강] test_target.py
- 쉘 스크립트(PowerShell / Bash)가 호출하는 대상 파이썬 스크립트
- 커맨드라인 인자(sys.argv), 환경 변수(os.environ), 그리고 종료 코드(sys.exit)의 원리를 실습합니다.
"""

import os
import sys

# Windows 콘솔 인코딩 대응
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def main():
    print("[Python] 파이썬 파이프라인 진입 완료!")

    # 1. 환경 변수 확인 (Environment Variables)
    stage = os.environ.get("STAGE", "development")
    api_key = os.environ.get("SECRET_KEY", "None (미설정)")
    print(f"[Python] 현재 환경 변수 STAGE: '{stage}'")
    print(f"[Python] 환경 변수 SECRET_KEY 설정 여부: {'✅ 설정됨' if api_key != 'None (미설정)' else '⚠️ 미설정'}")

    # 2. 커맨드라인 인자 확인 (CLI Arguments)
    args = sys.argv[1:]
    print(f"[Python] 전달받은 CLI 인자: {args}")

    # 3. 종료 코드(Exit Code) 분기 시뮬레이션
    if "--fail" in args:
        print("[Python] ❌ '--fail' 플래그가 감지되었습니다. 에러 종료 코드(Exit Code 1)를 반환합니다.", file=sys.stderr)
        sys.exit(1)

    print("[Python] ✅ 모든 작업이 정상 완료되었습니다. 성공 종료 코드(Exit Code 0)를 반환합니다.")
    sys.exit(0)


if __name__ == "__main__":
    main()
