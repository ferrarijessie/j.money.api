from mypy_extensions import TypedDict


class IncomeTypeInterface(TypedDict):
    name: str
    recurrent: bool
    base_value: float
    user_id: int

class IncomeInterface(TypedDict):
    type_id: int
    value: float
    month: int
    year: int
    received: bool

class IncomeUpdateInterface(TypedDict):
    value: float
    received: bool    
