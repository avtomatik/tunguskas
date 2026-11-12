from enum import Enum, StrEnum


class Location(StrEnum):
    LOWER_TUNGUSKA = "Нижняя Тунгуска"
    STONY_TUNGUSKA = "Подкаменная Тунгуска"


class TableShape(Enum):
    DATA = 40, 13
    STAMPS = 5, 2
