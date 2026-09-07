class ApplicationError(Exception):
    status_code: int = 500
    detail: str = "Application error"

    def __init__(self, detail: str | None = None) -> None:
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail)


class EntityNotFoundError(ApplicationError):
    status_code = 404
