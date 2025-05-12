# backend/app/exceptions.py
from fastapi import HTTPException, status

class ResourceNotFoundException(HTTPException):
    def __init__(self, resource_name: str, field_name: str, field_value: str):
        detail = f"{resource_name} not found with {field_name}: '{field_value}'"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class BlogAPIException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )

class DuplicatedUserInfoException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=message
        )

class FileStorageException(HTTPException):
    def __init__(self, message: str, cause: str = None):
        detail = f"{message}. Cause: {cause}" if cause else message
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )

class UserNotFoundException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message
        )