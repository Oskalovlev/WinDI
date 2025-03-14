from fastapi import status
from fastapi.exceptions import HTTPException


class ExceptionStatuses:

    def __init__(self, detail: str = None, optional_headers: str = None):
        self.detail = detail
        self.optional_headers = optional_headers

    def status_400(self):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=self.detail
        )

    def status_401(self):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=self.detail,
            headers=self.optional_headers
        )

    def status_403(self):
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=self.detail
        )

    def status_404(self):
        return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=self.detail
            )
