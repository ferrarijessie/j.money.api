from mypy_extensions import TypedDict

from .model import ExpenseCategoryEnum


class ExpenseTypeInterface(TypedDict):
    name: str
    category: ExpenseCategoryEnum
    recurrent: bool
    base_value: float


class ExpenseInterface(TypedDict):
    type_id: int
    value: float
    month: int
    year: int
    paid: bool


class ExpenseUpdateInterface(TypedDict):
    value: float
    paid: bool


class ExpenseReturnInterface(TypedDict):
    id: int
    type: str
    value: float
    month: int
    year: int
    paid: bool
    category: str
