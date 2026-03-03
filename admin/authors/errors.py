from fastapi import HTTPException


class NotFoundInDbError(HTTPException):
    ...

