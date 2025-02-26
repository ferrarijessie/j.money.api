from mypy_extensions import TypedDict


class CreateUserInterface(TypedDict):
    username: str
    password: str
    first_name: str
    last_name: str
    email: str

class UpdateUserInterface(TypedDict):
    username: str
    first_name: str
    last_name: str
    email: str
