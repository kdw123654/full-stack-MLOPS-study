"""
[MLOps Full-Stack 01강] 개발 환경 & 시스템 진단 스크립트 (check_env.py)

이 스크립트는 다음 항목을 진단합니다:
1. Python 실행 환경 (버전, 가상환경 활성화 여부)
2. 호스트 OS 및 하드웨어 사양 (CPU 코어, RAM 용량)
3. GPU / AI 가속 하드웨어 (NVIDIA CUDA, PyTorch 연동 여부)
4. Git 및 버전 관리 상태 (Git 설치 여부, 현재 브랜치, 커밋 해시)
5. 결과를 'system_diagnostic_report.md'로 저장
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
# Windows cp949 인코딩 환경 대응
if sys.platform == "win32":
    try:
        if sys.stdout and hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if sys.stderr and hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# 터미널 컬러 출력을 위한 rich 라이브러리 (미설치 시 표준 출력 폴백)
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    console = Console(legacy_windows=False)
    HAS_RICH = True
except Exception:
    console = None
    HAS_RICH = False

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False


def check_python_environment():
    """Python 버전 및 가상환경(venv) 활성화 상태 확인"""
    py_version = sys.version.split()[0]
    executable = sys.executable
    in_venv = (
        hasattr(sys, 'real_prefix') or 
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) or
        os.environ.get("VIRTUAL_ENV") is not None
    )
    venv_path = os.environ.get("VIRTUAL_ENV", sys.prefix if in_venv else "None (글로벌 파이썬 실행 중)")
    
    # 파이썬 권장 버전 체크 (3.10 ~ 3.12 권장)
    major, minor = sys.version_info.major, sys.version_info.minor
    is_supported = (major == 3 and 10 <= minor <= 12)
    
    return {
        "version": py_version,
        "is_supported": is_supported,
        "executable": executable,
        "in_venv": in_venv,
        "venv_path": venv_path,
    }


def check_system_hardware():
    """OS, CPU, 메모리(RAM) 사양 확인"""
    os_name = platform.system()
    os_release = platform.release()
    arch = platform.machine()
    
    cpu_cores_physical = psutil.cpu_count(logical=False) if HAS_PSUTIL else "N/A"
    cpu_cores_logical = psutil.cpu_count(logical=True) if HAS_PSUTIL else os.cpu_count()
    
    if HAS_PSUTIL:
        mem = psutil.virtual_memory()
        total_ram_gb = round(mem.total / (1024 ** 3), 2)
        avail_ram_gb = round(mem.available / (1024 ** 3), 2)
    else:
        total_ram_gb = "N/A (psutil 필요)"
        avail_ram_gb = "N/A (psutil 필요)"
        
    return {
        "os": f"{os_name} {os_release} ({arch})",
        "cpu_cores": f"물리 {cpu_cores_physical}코어 / 논리 {cpu_cores_logical}스레드",
        "total_ram": f"{total_ram_gb} GB",
        "avail_ram": f"{avail_ram_gb} GB",
    }


def check_gpu_and_acceleration():
    """NVIDIA GPU 및 PyTorch CUDA 가속 여부 확인"""
    gpu_info = {
        "has_nvidia_smi": False,
        "nvidia_smi_output": "NVIDIA GPU 드라이버를 감지하지 못했습니다.",
        "has_torch": HAS_TORCH,
        "torch_version": torch.__version__ if HAS_TORCH else "미설치 (추후 학습 시 설치)",
        "cuda_available": False,
        "device_count": 0,
        "device_names": [],
    }
    
    # 1. nvidia-smi CLI 확인
    if shutil.which("nvidia-smi"):
        gpu_info["has_nvidia_smi"] = True
        try:
            res = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"],
                capture_output=True, text=True, timeout=5
            )
            if res.returncode == 0:
                gpu_info["nvidia_smi_output"] = res.stdout.strip()
        except Exception:
            gpu_info["nvidia_smi_output"] = "nvidia-smi 실행 오류"
            
    # 2. PyTorch CUDA 감지
    if HAS_TORCH:
        if torch.cuda.is_available():
            gpu_info["cuda_available"] = True
            gpu_info["device_count"] = torch.cuda.device_count()
            gpu_info["device_names"] = [
                torch.cuda.get_device_name(i) for i in range(gpu_info["device_count"])
            ]
            
    return gpu_info


def check_git_status():
    """Git 설치 및 현재 스터디 레포지토리 상태 확인"""
    git_installed = shutil.which("git") is not None
    if not git_installed:
        return {"installed": False, "status": "Git이 설치되어 있지 않거나 PATH에 없습니다."}
        
    try:
        ver_res = subprocess.run(["git", "--version"], capture_output=True, text=True, check=True)
        git_version = ver_res.stdout.strip()
        
        branch_res = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True)
        current_branch = branch_res.stdout.strip() or "(분기 없음/새 레포지토리)"
        
        status_res = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)
        status_summary = f"{len(status_res.stdout.strip().splitlines())}개 파일 변경사항 감지됨" if status_res.stdout.strip() else "작업 트리가 깨끗함 (Clean)"
        
        return {
            "installed": True,
            "version": git_version,
            "branch": current_branch,
            "status_summary": status_summary,
        }
    except Exception as e:
        return {
            "installed": True,
            "version": "Git 감지됨",
            "branch": "확인 불가",
            "status_summary": f"Git 명령 실행 오류: {e}",
        }


def print_report_terminal(py_env, hw_env, gpu_env, git_env):
    """터미널에 진단 결과 출력"""
    success_rich = False
    if HAS_RICH and console:
        try:
            console.print(Panel.fit("[bold cyan]🚀 MLOps Full-Stack 01강: 개발 환경 진단 결과[/bold cyan]"))
            
            # 1. 파이썬 환경
            table_py = Table(title="🐍 1. Python 환경", show_header=True, header_style="bold magenta")
            table_py.add_column("항목", style="dim", width=20)
            table_py.add_column("진단 값", style="bold")
            table_py.add_row("Python 버전", f"{py_env['version']} ({'✅ 권장 버전' if py_env['is_supported'] else '⚠️ 3.10~3.12 권장'})")
            table_py.add_row("가상환경(venv) 활성화", "✅ 격리 가상환경 활성화됨" if py_env['in_venv'] else "[bold red]❌ 가상환경 미적용 (글로벌)[/bold red]")
            table_py.add_row("실행 인터프리터 경로", py_env['executable'])
            console.print(table_py)
            
            # 2. 하드웨어 환경
            table_hw = Table(title="💻 2. 하드웨어 & OS", show_header=True, header_style="bold green")
            table_hw.add_column("항목", style="dim", width=20)
            table_hw.add_column("진단 값", style="bold")
            table_hw.add_row("운영체제(OS)", hw_env['os'])
            table_hw.add_row("CPU 코어", hw_env['cpu_cores'])
            table_hw.add_row("전체 RAM", hw_env['total_ram'])
            table_hw.add_row("사용 가능 RAM", hw_env['avail_ram'])
            console.print(table_hw)
            
            # 3. GPU 가속
            table_gpu = Table(title="⚡ 3. GPU / AI 가속", show_header=True, header_style="bold yellow")
            table_gpu.add_column("항목", style="dim", width=20)
            table_gpu.add_column("진단 값", style="bold")
            table_gpu.add_row("NVIDIA 드라이버", gpu_env['nvidia_smi_output'])
            table_gpu.add_row("PyTorch 설치 상태", gpu_env['torch_version'])
            table_gpu.add_row("CUDA 가속 가능 여부", "✅ 사용 가능 (GPU 연산 활성화)" if gpu_env['cuda_available'] else "ℹ️ CPU 전용 (또는 CUDA 미연동)")
            if gpu_env['cuda_available']:
                table_gpu.add_row("GPU 장치명", ", ".join(gpu_env['device_names']))
            console.print(table_gpu)
            
            # 4. Git 상태
            table_git = Table(title="🌿 4. Git & GitHub 연동", show_header=True, header_style="bold blue")
            table_git.add_column("항목", style="dim", width=20)
            table_git.add_column("진단 값", style="bold")
            table_git.add_row("Git 설치", f"✅ {git_env['version']}" if git_env['installed'] else "❌ Git 미설치")
            if git_env['installed']:
                table_git.add_row("현재 작업 브랜치", git_env['branch'])
                table_git.add_row("작업 디렉토리 상태", git_env['status_summary'])
            console.print(table_git)
            success_rich = True
        except Exception:
            success_rich = False
            
    if not success_rich:
        print("\n" + "="*60)
        print("[MLOps Full-Stack] 01강: 개발 환경 진단 결과")
        print("="*60)
        print(f"[Python] 버전: {py_env['version']} | venv 활성화: {py_env['in_venv']}")
        print(f"[OS/HW] {hw_env['os']} | CPU: {hw_env['cpu_cores']} | RAM: {hw_env['total_ram']}")
        print(f"[GPU] {gpu_env['nvidia_smi_output']} | CUDA: {gpu_env['cuda_available']}")
        print(f"[Git] {git_env.get('version', 'N/A')} | 브랜치: {git_env.get('branch', 'N/A')}")
        print("="*60 + "\n")


def generate_markdown_report(py_env, hw_env, gpu_env, git_env, output_path: Path):
    """결과를 Markdown 리포트 파일로 자동 저장"""
    md_content = f"""# 📋 MLOps 환경 진단 리포트 (System Diagnostic Report)

- **생성 일시**: `{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}`
- **진단자**: MLOps 풀스택 스터디원

---

## 1. 🐍 Python 환경
| 항목 | 진단 값 | 상태 |
| :--- | :--- | :--- |
| **Python 버전** | `{py_env['version']}` | {'✅ 권장 버전 (3.10~3.12)' if py_env['is_supported'] else '⚠️ 확인 필요'} |
| **가상환경(venv) 격리** | `{'활성화됨' if py_env['in_venv'] else '비활성화 (글로벌)'}` | {'✅ 통과' if py_env['in_venv'] else '❌ 가상환경 필수'} |
| **인터프리터 위치** | `{py_env['executable']}` | - |
| **가상환경 경로** | `{py_env['venv_path']}` | - |

## 2. 💻 하드웨어 및 운영체제
| 항목 | 사양 |
| :--- | :--- |
| **운영체제(OS)** | `{hw_env['os']}` |
| **CPU 코어** | `{hw_env['cpu_cores']}` |
| **전체 RAM** | `{hw_env['total_ram']}` |
| **가용 RAM** | `{hw_env['avail_ram']}` |

## 3. ⚡ GPU 및 가속 하드웨어
| 항목 | 상태 |
| :--- | :--- |
| **NVIDIA 드라이버 정보** | `{gpu_env['nvidia_smi_output']}` |
| **PyTorch 설치 여부** | `{gpu_env['torch_version']}` |
| **CUDA 가속 지원** | `{'✅ 지원 (GPU Acceleration Enabled)' if gpu_env['cuda_available'] else 'ℹ️ CPU 모드 (또는 추후 세팅)'}` |
| **감지된 GPU 수 / 이름** | `{gpu_env['device_count']}대 / {', '.join(gpu_env['device_names']) if gpu_env['device_names'] else '없음'}` |

## 4. 🌿 Git 및 저장소 상태
| 항목 | 상태 |
| :--- | :--- |
| **Git 버전** | `{git_env.get('version', '미설치')}` |
| **현재 작업 브랜치** | `{git_env.get('branch', 'N/A')}` |
| **작업 트리 변경 사항** | `{git_env.get('status_summary', 'N/A')}` |

---
> 💡 *이 리포트는 `python 01_environment_and_git/scripts/check_env.py` 실행에 의해 자동 생성되었습니다.*
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"\n[INFO] 환경 진단 보고서가 성공적으로 저장되었습니다: {output_path}")


def main():
    py_env = check_python_environment()
    hw_env = check_system_hardware()
    gpu_env = check_gpu_and_acceleration()
    git_env = check_git_status()
    
    print_report_terminal(py_env, hw_env, gpu_env, git_env)
    
    report_file = Path(__file__).resolve().parent.parent / "system_diagnostic_report.md"
    generate_markdown_report(py_env, hw_env, gpu_env, git_env, report_file)


if __name__ == "__main__":
    main()
