class APIError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class RateLimitError(APIError):
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message)


class BadRequestError(APIError):
    def __init__(self, message: str = "Bad request"):
        super().__init__(message)


class UnexpectedStatusError(APIError):
    def __init__(self, message: str):
        super().__init__(message)