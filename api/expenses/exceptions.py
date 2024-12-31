class ExpenseTypeNotFoundException(Exception):
    def __init__(self, message="Expense type not found"):
        super().__init__(message)


class ExpenseNotFoundException(Exception):
    def __init__(self, message="Expense not found"):
        super().__init__(message)