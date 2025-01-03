from mypy_extensions import TypedDict


class IncomeTypeInterface:
    name: str
    recurrent: bool

class IncomeInterface(TypedDict):
    type_id: int
    value: float
    month: int
    year: int
    received: bool

class IncomeUpdateInterface(TypedDict):
    value: float
    received: bool    
