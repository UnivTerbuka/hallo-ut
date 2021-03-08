from enum import Enum


class PriorityTiket(Enum):
    _init_ = "value string"
    LOW = 1, "Low"
    MEDIUM = 2, "Medium"
    HIGH = 3, "High"

    def __str__(self) -> str:
        return self.string  # type: ignore
