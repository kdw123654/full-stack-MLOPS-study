# 📝 [제3강 과제] 스마트 팩토리 IoT 센서 데이터 검증 파이프라인 구현

축하합니다! 2강에서는 MLOps 서빙의 핵심 문지기인 **타입 힌트, 객체지향 설계, Pydantic v2 데이터 검증**을 배웠습니다.  
이번 과제는 배운 내용을 응용하여 **스마트 팩토리의 IoT 센서 이상치 탐지 AI 서빙을 위한 입력 검증기**를 직접 완성해 보는 챌린지입니다.

---

## 🎯 과제 목표
스마트 팩토리 장비에서 1초마다 전송되는 센서 데이터 중, **비정상 데이터와 결측치, 논리적 모순을 Pydantic v2 모델로 차단**하는 `SensorPayload` 클래스를 구현하세요.

### 📋 세부 요구 조건
1. **클래스명**: `SensorPayload(BaseModel)`
2. **필드 정의**:
   - `device_id` (문자열): 필수값. 반드시 `"SENSOR-"`로 시작해야 함. (미준수 시 `ValueError` 발생)
   - `temperature` (실수): 섭씨온도. `-40.0`도 이상 `150.0`도 이하만 허용 (`ge`, `le` 사용).
   - `vibration` (실수): 진동 수치. `0.0` 이상만 허용 (`ge` 사용).
   - `status` (리터럴): `"NORMAL"`, `"WARNING"`, `"CRITICAL"` 중 하나만 허용 (`Literal` 사용).
   - `timestamp` (문자열 또는 datetime): 측정 일시.
3. **복합 논리 검증 (`@model_validator(mode="after")`)**:
   - 만약 `temperature >= 100.0` (과열 상태)인데, 장비 상태(`status`)가 `"NORMAL"`로 보고되면 명백한 센서 오작동이므로 `ValueError("온도가 100도 이상인데 NORMAL 상태일 수 없습니다.")`를 발생시킬 것.

---

## 💻 실습 코드 템플릿 (`assignments/solution_02.py`에 작성)

```python
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field, field_validator, model_validator, ValidationError


class SensorPayload(BaseModel):
    # TODO: 필드들을 정의하세요.
    pass

    # TODO: @field_validator("device_id") 구현
    
    # TODO: @model_validator(mode="after") 구현


# =======================================================
# 테스트 코드 (아래 테스트가 모두 통과해야 합니다)
# =======================================================
if __name__ == "__main__":
    # 1. 정상 데이터 테스트 (통과해야 함)
    valid_data = {
        "device_id": "SENSOR-001",
        "temperature": 75.5,
        "vibration": 1.2,
        "status": "NORMAL",
        "timestamp": datetime.now()
    }
    sensor = SensorPayload(**valid_data)
    print("✅ 1. 정상 데이터 파싱 성공:", sensor.device_id)

    # 2. 과열 모순 데이터 테스트 (차단되어야 함)
    abnormal_data = {
        "device_id": "SENSOR-002",
        "temperature": 115.0, # 과열!
        "vibration": 3.4,
        "status": "NORMAL",   # 모순!
        "timestamp": datetime.now()
    }
    try:
        SensorPayload(**abnormal_data)
        print("❌ 과열 모순 데이터가 통과되었습니다. (실패)")
    except ValidationError as e:
        print("✅ 2. 과열 모순 데이터 정상 차단 완료!")
```

---

## 🚀 과제 제출 및 Git 커밋
코드를 완성하고 실행하여 모두 통과하면 GitHub에 커밋하고 푸시합니다:

```powershell
# 1. 루트 폴더에서 변경사항 확인
git status

# 2. 스테이징 & 커밋
git add .
git commit -m "feat: complete lesson 02 modern python, oop, and pydantic homework"

# 3. 깃허브로 푸시
git push origin main
```

체크리스트가 완료되면 2강 정복 완료입니다! 🎉
