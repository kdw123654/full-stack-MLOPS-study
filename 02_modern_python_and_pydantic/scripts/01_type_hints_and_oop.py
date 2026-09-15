"""
[MLOps Full-Stack 02강] 01_type_hints_and_oop.py
- 파이썬 타입 힌팅(Type Hints) 실무 기법
- 객체지향 설계(OOP)와 추상화(Abstract Base Class)
- MLOps 모델 전처리기 설계 패턴 (Strategy / Pipeline 패턴)
"""

import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union, Literal

# Windows cp949 인코딩 콘솔 대응
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    console = Console(legacy_windows=False)
    HAS_RICH = True
except Exception:
    console = None
    HAS_RICH = False


# =====================================================================
# 1. dataclass를 활용한 클린 설정(Config) 관리
# =====================================================================
@dataclass(frozen=True)
class TrainingConfig:
    """
    불변(Immutable) 학습 설정 클래스.
    frozen=True로 설정하여 학습 도중 설정값이 임의로 변경되는 버그를 원천 차단합니다.
    """
    model_name: str
    learning_rate: float
    batch_size: int
    epochs: int = 10
    optimizer: Literal["adam", "adamw", "sgd"] = "adamw"
    tags: List[str] = field(default_factory=lambda: ["experiment", "baseline"])


# =====================================================================
# 2. 객체지향(OOP) 전처리기 인터페이스 정의 (추상 기반 클래스)
# =====================================================================
class BasePreprocessor(ABC):
    """
    모든 MLOps 데이터 전처리기가 반드시 따라야 하는 규격(Interface).
    새로운 전처리 알고리즘이 추가되어도 동일한 fit_transform 인터페이스를 보장합니다.
    """
    @abstractmethod
    def fit(self, data: List[float]) -> "BasePreprocessor":
        """데이터의 통계량(평균, 최댓값 등)을 학습합니다."""
        pass

    @abstractmethod
    def transform(self, data: List[float]) -> List[float]:
        """학습된 통계량을 바탕으로 데이터를 변환합니다."""
        pass

    def fit_transform(self, data: List[float]) -> List[float]:
        """fit과 transform을 연속으로 수행합니다."""
        return self.fit(data).transform(data)


# =====================================================================
# 3. 구체적인 전처리기 구현 (표준화 & Min-Max 정규화)
# =====================================================================
class StandardScaler(BasePreprocessor):
    """표준 정규분포(평균 0, 표준편차 1) 스케일러"""
    def __init__(self) -> None:
        self.mean: Optional[float] = None
        self.std: Optional[float] = None

    def fit(self, data: List[float]) -> "StandardScaler":
        if not data:
            raise ValueError("데이터가 비어 있어 통계량을 계산할 수 없습니다.")
        self.mean = sum(data) / len(data)
        variance = sum((x - self.mean) ** 2 for x in data) / len(data)
        self.std = variance ** 0.5 or 1e-7  # 0으로 나누기 방지
        return self

    def transform(self, data: List[float]) -> List[float]:
        if self.mean is None or self.std is None:
            raise RuntimeError("fit()이 먼저 호출되어야 합니다.")
        return [(x - self.mean) / self.std for x in data]


class MinMaxScaler(BasePreprocessor):
    """0과 1 사이로 압축하는 Min-Max 스케일러"""
    def __init__(self) -> None:
        self.min_val: Optional[float] = None
        self.max_val: Optional[float] = None

    def fit(self, data: List[float]) -> "MinMaxScaler":
        if not data:
            raise ValueError("데이터가 비어 있습니다.")
        self.min_val = min(data)
        self.max_val = max(data)
        return self

    def transform(self, data: List[float]) -> List[float]:
        if self.min_val is None or self.max_val is None:
            raise RuntimeError("fit()이 먼저 호출되어야 합니다.")
        diff = self.max_val - self.min_val
        if diff == 0:
            return [0.0 for _ in data]
        return [(x - self.min_val) / diff for x in data]


# =====================================================================
# 4. 전처리기 팩토리 패턴 (Preprocessor Factory)
# =====================================================================
class PreprocessorFactory:
    """문자열 이름에 따라 적절한 전처리 객체를 생성해 반환하는 팩토리 클래스"""
    _registry: Dict[str, type] = {
        "standard": StandardScaler,
        "minmax": MinMaxScaler,
    }

    @classmethod
    def get_scaler(cls, method: Literal["standard", "minmax"]) -> BasePreprocessor:
        scaler_cls = cls._registry.get(method)
        if not scaler_cls:
            raise ValueError(f"지원하지 않는 스케일러: {method}. 가능한 값: {list(cls._registry.keys())}")
        return scaler_cls()


# =====================================================================
# 5. 실행 및 결과 검증
# =====================================================================
def main():
    raw_features: List[float] = [10.0, 25.0, 32.0, 48.0, 100.0]
    
    # 1. 설정 로드
    config = TrainingConfig(
        model_name="xgboost_regressor",
        learning_rate=0.01,
        batch_size=64,
        epochs=50,
        optimizer="adamw",
        tags=["production", "v1.0.0"]
    )
    
    # 2. 팩토리를 통한 스케일러 생성 및 변환
    scaler = PreprocessorFactory.get_scaler("minmax")
    scaled_features = scaler.fit_transform(raw_features)
    
    # 3. 터미널 출력
    if HAS_RICH and console:
        console.print(Panel.fit("[bold green]🎯 MLOps 풀스택 02강: 타입 힌트 & OOP 전처리기 시연[/bold green]"))
        
        table_cfg = Table(title="📌 모델 학습 불변 설정 (dataclass)", header_style="bold magenta")
        table_cfg.add_column("설정 키")
        table_cfg.add_column("값")
        table_cfg.add_row("모델명", config.model_name)
        table_cfg.add_row("학습률 (LR)", str(config.learning_rate))
        table_cfg.add_row("배치 크기", str(config.batch_size))
        table_cfg.add_row("옵티마이저", config.optimizer)
        table_cfg.add_row("태그", ", ".join(config.tags))
        console.print(table_cfg)
        
        table_data = Table(title="🔄 전처리 변환 전/후 (Min-Max Scaling)", header_style="bold cyan")
        table_data.add_column("인덱스", justify="center")
        table_data.add_column("원본 Feature", justify="right")
        table_data.add_column("변환 후 Feature (0~1)", justify="right", style="bold yellow")
        for i, (orig, sc) in enumerate(zip(raw_features, scaled_features)):
            table_data.add_row(str(i + 1), f"{orig:.1f}", f"{sc:.4f}")
        console.print(table_data)
    else:
        print("=== [02강] 타입 힌트 & OOP 전처리기 시연 ===")
        print(f"모델 설정: {config}")
        print(f"원본 데이터: {raw_features}")
        print(f"Min-Max 스케일링 결과: {[round(x, 4) for x in scaled_features]}")


if __name__ == "__main__":
    main()
