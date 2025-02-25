from mypy_extensions import TypedDict


class SavingTypeInterface(TypedDict):
    name: str
    active: bool
    base_value: float
    user_id: int


class SavingValueInterface(TypedDict):
    value: float
    month: int
    year: int
    type_id: int
    used: bool


class SavingValueUpdateInterface(TypedDict):
    value: float
    used: bool
