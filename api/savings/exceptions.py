class SavingTypeNotFoundException(Exception):
    def __init__(self, message="Saving type not found"):
        super().__init__(message)


class SavingValueNotFoundException(Exception):
    def __init__(self, message="Saving not found"):
        super().__init__(message)