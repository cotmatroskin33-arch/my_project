from http import HTTPStatus


class ApplicationError(Exception):
    status_code: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR
    message: str = "Application error"

    def __init__(self, message: str | None = None) -> None:
        if message is not None:
            self.message = message
        super().__init__(self.message)


class EntityNotFoundError(ApplicationError):
    status_code = HTTPStatus.NOT_FOUND
