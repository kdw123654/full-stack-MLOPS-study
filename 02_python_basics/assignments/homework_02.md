# 📝 [제2강 과제] 미니 데이터 분석기: 학생 성적 분석 리포트 제작

축하합니다! 2강에서는 파이썬의 가장 중요한 뼈대인 **변수, 자료형, 조건문, 반복문, 자료구조(List, Dict, Set), 함수, 파일IO**를 완벽하게 정복했습니다.  
이번 과제는 배운 내용을 종합하여 **학생들의 시험 점수를 분석하고 통계를 내는 미니 파이썬 프로그램**을 완성하는 실습 미션입니다.

---

## 🎯 과제 목표
아래 주어진 미가공 학생 데이터(`raw_students`)를 가공하여:
1. 각 학생의 **평균 점수**를 계산하고,
2. 평균 80점 이상인 학생에게 `"합격(PASS)"`, 미만인 학생에게 `"재시험(RETEST)"`을 부여하며,
3. **리스트 컴프리헨션**을 사용하여 합격자 명단만 따로 추출하는 함수를 작성하세요.

---

## 💻 실습 코드 템플릿 (`assignments/solution_02.py`에 작성)

```python
# ===============================================================
# 학생 성적 원본 데이터 (이름, 수학, 영어, 파이썬)
# ===============================================================
raw_students = [
    {"name": "김철수", "scores": [85, 90, 95]},
    {"name": "이영희", "scores": [70, 65, 80]},
    {"name": "박민수", "scores": [95, 100, 98]},
    {"name": "최지우", "scores": [50, 60, 55]},
    {"name": "정다은", "scores": [88, 84, 92]},
]


# 1. 평균을 계산하는 함수를 완성하세요
def calculate_average(score_list: list) -> float:
    # TODO: 합계(sum)와 개수(len)를 이용해 평균을 구하고 반환하세요.
    return round(sum(score_list) / len(score_list), 2)


# 2. 메인 분석 함수를 완성하세요
def analyze_students(students: list):
    analyzed_results = []

    for s in students:
        avg = calculate_average(s["scores"])
        # TODO: avg가 80점 이상이면 "PASS", 아니면 "RETEST" 부여
        status = "PASS" if avg >= 80.0 else "RETEST"
        
        analyzed_results.append({
            "name": s["name"],
            "average": avg,
            "status": status
        })

    # 3. 리스트 컴프리헨션을 사용하여 "PASS"인 학생 이름만 추출하세요
    # TODO: [student["name"] for student in analyzed_results if ...]
    passed_names = [s["name"] for s in analyzed_results if s["status"] == "PASS"]

    return analyzed_results, passed_names


if __name__ == "__main__":
    results, passed = analyze_students(raw_students)
    
    print("=" * 45)
    print("📊 학생 성적 분석 결과")
    print("=" * 45)
    for r in results:
        print(f"학생: {r['name']} | 평균: {r['average']:>5.2f}점 | 상태: {r['status']}")
    print("-" * 45)
    print(f"🎉 최종 합격자 명단: {passed} (총 {len(passed)}명)")
    print("=" * 45)
```

---

## 🚀 과제 제출 및 Git 커밋

코드를 실행하여 합격자 명단(`['김철수', '박민수', '정다은']`)이 정확히 나오면 GitHub에 커밋하고 푸시합니다:

```powershell
# 1. 루트 폴더에서 상태 확인
git status

# 2. 스테이징 & 커밋
git add .
git commit -m "feat: complete lesson 02 python basics core and homework"

# 3. GitHub로 푸시
git push origin main
```

축하합니다! 이제 파이썬의 가장 탄탄한 기본기가 완성되었습니다! 🎉
