import enum

from dataclasses import dataclass


class SummaryItemModelEnum(enum.Enum):
    EXPENSE = 'expense'
    INCOME = 'income'
    SAVING = 'saving'

@dataclass
class SummaryItem:
    id: int
    value: float
    type_name: str
    type_id: int
    month: int
    year: int
    status: bool
    model: SummaryItemModelEnum
