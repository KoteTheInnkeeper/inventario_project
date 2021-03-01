class DatabaseInitError(Exception):
    """
        This error may be raised when we encountered an error when initializing the database.
    """

    def __init__(self, message: str):
        super().__init__(message)


class ProductExists(Exception):
    """
        If the product already exists in database, this error would be raised.
    """

    def __init__(self, message: str):
        super().__init__(message)


class UnableToAdd(Exception):
    """
        An error for not being able to add a product.
    """

    def __init__(self, message: str):
        super().__init__(message)


# USERS ERRORS
class UnmatchedUsername(Exception):
    """
        An error for not being able to find a match for a given username.
    """
    def __init__(self, message: str):
        super().__init__(message)


class UnmatchedPassword(Exception):
    """
        An error for not being able to find a match for a given password.
    """
    def __init__(self, message: str):
        super().__init__(message)


class UserNotUnique(Exception):
    """
        An error for when, after a try of creating a new user, we found a match.
    """
    def __init__(self, message: str):
        super().__init__(message)
