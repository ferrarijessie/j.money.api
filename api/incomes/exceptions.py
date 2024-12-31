class IncomeTypeNotFoundException(Exception):
    def __init__(self, message="Income type not found"):
        super().__init__(message)


class IncomeNotFoundException(Exception):
    def __init__(self, message="Income not found"):
        super().__init__(message)