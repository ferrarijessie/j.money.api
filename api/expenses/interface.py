from mypy_extensions import TypedDict

from .model import ExpenseCategoryEnum


class ExpenseTypeInterface(TypedDict):
    name: str
    category: ExpenseCategoryEnum
    recurrent: bool
    base_value: float
    user_id: int


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
    type_name: str
    type_id: int
    value: float
    month: int
    year: int
    paid: bool
    category: str
