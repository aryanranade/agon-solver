from enum import Enum, auto

class TaskType(Enum):
    ARITHMETIC = auto()
    EXTRACTION = auto()
    CLASSIFICATION = auto()
    LIST_OPS = auto()
    COMPARISON = auto()
    RULE_ENGINE = auto()
    POLY_GCD = auto()
    REASONING = auto()
    UNKNOWN = auto()
