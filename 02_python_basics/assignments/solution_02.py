"""
[MLOps Full-Stack 02강 과제 정답] solution_02.py
- 학생 성적 데이터 가공, 평균 계산 함수, 조건문, 리스트 컴프리헨션 완성본
"""

import sys

# Windows 콘솔 한글/인코딩 대응
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ===============================================================
# 학생 성적 원본 데이터 (이름, [수학, 영어, 파이썬 점수])
# ===============================================================
raw_students = [
    {"name": "김철수", "scores": [85, 90, 95]},
    {"name": "이영희", "scores": [70, 65, 80]},
    {"name": "박민수", "scores": [95, 100, 98]},
    {"name": "최지우", "scores": [50, 60, 55]},
    {"name": "정다은", "scores": [88, 84, 92]},
]


# ===============================================================
# [문제 1] 점수 리스트의 평균을 계산하는 함수
# ===============================================================
def calculate_average(score_list: list) -> float:
    """
    내장 함수 sum()으로 리스트 전체 합을 구하고,
    len()으로 과목 수를 나누어 평균을 계산합니다.
    round(값, 2)를 사용하여 소수점 둘째 자리까지 반올림합니다.
    """
    if not score_list:  # 만약 점수 리스트가 비어있다면 0.0 반환 (0으로 나누기 방지)
        return 0.0
    
    total = sum(score_list)
    count = len(score_list)
    average = total / count
    
    return round(average, 2)


# ===============================================================
# [문제 2 & 3] 전체 학생 데이터 분석 및 합격자 추출 함수
# ===============================================================
def analyze_students(students: list) -> tuple:
    analyzed_results = []

    for s in students:
        # 1. 앞에서 만든 calculate_average 함수를 호출하여 평균 계산
        avg = calculate_average(s["scores"])
        
        # 2. 조건문: 80점 이상이면 "PASS", 미만이면 "RETEST" (삼항 연산자)
        status = "PASS" if avg >= 80.0 else "RETEST"
        
        analyzed_results.append({
            "name": s["name"],
            "average": avg,
            "status": status
        })

    # 3. [핵심] 리스트 컴프리헨션(List Comprehension)
    # analyzed_results 목록 중에서 status가 "PASS"인 학생의 name만 쏙쏙 뽑아 새로운 리스트 생성
    passed_names = [s["name"] for s in analyzed_results if s["status"] == "PASS"]

    return analyzed_results, passed_names


# ===============================================================
# 실행 및 결과 출력
# ===============================================================
if __name__ == "__main__":
    results, passed = analyze_students(raw_students)
    
    print("=" * 50)
    print("📊 [제2강 과제 정답] 학생 성적 분석 결과 리포트")
    print("=" * 50)
    
    for r in results:
        # 상태에 따라 보기 쉽게 이모지 추가
        icon = "✅" if r["status"] == "PASS" else "❌"
        # :>6.2f -> 총 6칸 너비 확보하고 오른쪽 정렬로 줄 맞춤
        print(f"{icon} 학생: {r['name']} | 평균: {r['average']:>6.2f}점 | 상태: {r['status']}")
        
    print("-" * 50)
    print(f"🎉 최종 합격자 명단 (80점 이상): {passed}")
    print(f"📈 총 합격자 수: {len(passed)}명 / 전체 {len(results)}명")
    print("=" * 50)
