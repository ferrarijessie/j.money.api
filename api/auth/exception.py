class UsernameAlreadyExistsException(Exception):
    def __init__(self, message="Username already exists!") :
        super().__init__(message)

class LoginException(Exception):
    def __init__(self, message="Wrong credentials!") :
        super().__init__(message)

class UserNotFoundException(Exception):
    def __init__(self, message="User not found!") :
        super().__init__(message)
