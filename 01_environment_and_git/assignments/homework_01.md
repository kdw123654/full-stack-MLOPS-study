# 📝 [제1강 과제] 나의 개발 환경 진단 및 GitHub 첫 푸시 챌린지

축하합니다! MLOps 풀스택 엔지니어링의 첫걸음을 떼셨습니다.  
이번 과제는 배운 내용을 바탕으로 **내 로컬 머신에 완벽한 격리 환경을 구축하고, 진단 결과를 GitHub 레포지토리에 기록**하는 실습 미션입니다.

---

## 🎯 과제 목표
- [x] Python 가상환경(`.venv`)을 생성하고 활성화할 수 있다.
- [x] `check_env.py`를 실행하여 내 컴퓨터의 하드웨어와 Python 상태를 진단한다.
- [x] 생성된 `system_diagnostic_report.md`를 확인하고 GitHub에 첫 커밋/푸시를 완료한다.

---

## 🛠️ 미션 수행 단계

### 1단계: 가상환경 생성 및 활성화
1. VS Code에서 터미널(`Ctrl + ~`)을 엽니다.
2. 프로젝트 루트 디렉토리(`mlops full-stack`)에서 다음 명령어를 실행합니다:
   ```powershell
   python -m venv .venv
   ```
3. 가상환경을 활성화합니다:
   ```powershell
   .venv\Scripts\Activate.ps1
   ```
   > 💡 터미널 프롬프트 맨 앞에 `(.venv)`가 보이면 성공입니다!

---

### 2단계: 1강 필수 패키지 설치
1강 디렉토리로 이동하여 환경 진단에 필요한 도구를 설치합니다:
```powershell
cd 01_environment_and_git
pip install -r requirements.txt
```

---

### 3단계: 환경 진단 도구 실행
터미널에서 아래 명령을 실행합니다:
```powershell
python scripts/check_env.py
```
- 터미널에 예쁜 표(Table)로 진단 결과가 출력되는지 확인합니다.
- `01_environment_and_git/system_diagnostic_report.md` 파일이 정상적으로 생성되었는지 확인합니다.

---

### 4단계: GitHub에 첫 커밋 & 푸시
프로젝트 루트 디렉토리로 돌아와서 변경사항을 커밋하고 본인의 원격 저장소에 푸시합니다:

```powershell
# 1. 루트 폴더로 이동
cd ..

# 2. 변경된 파일 상태 확인
git status

# 3. 모든 파일 스테이징
git add .

# 4. 커밋 메시지 작성
git commit -m "docs: complete lesson 01 environment setup and diagnostic report"

# 5. 원격 저장소로 푸시
git push origin main
```
*(만약 브랜치 이름이 `master`라면 `git push origin master`)*

---

## 🌟 과제 완료 체크리스트
- [ ] `.venv` 폴더가 Git 커밋 목록(`git status`)에 **포함되지 않았는지** 확인 (`.gitignore` 작동 확인)
- [ ] `system_diagnostic_report.md` 파일에 내 컴퓨터 사양과 Python 버전이 잘 기록되었는가?
- [ ] 내 GitHub 스터디 레포지토리에 1강 폴더와 파일들이 잘 올라갔는가?

모든 체크리스트를 완료하셨다면 1강 미션 완수입니다! 🎉  
다음 **제2강: 모던 파이썬 & 객체지향 설계(OOP) 및 Pydantic 데이터 검증**에서 만나요!
