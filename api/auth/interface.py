from mypy_extensions import TypedDict


class CreateUserInterface(TypedDict):
    username: str
    password: str

class UpdateUserInterface(TypedDict):
    username: str
