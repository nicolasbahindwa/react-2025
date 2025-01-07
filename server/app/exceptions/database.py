from fastapi import HTTPException, status

class DatabaseError(HTTPException):
    def __init__(self, detail: str = "A database error occurred"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class NotFoundException(HTTPException):
    def __init__(self, model_name: str, id: any):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=f"{model_name} with id {id} not found")

class InvalidFieldException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)

class InvalidDataException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)

class DatabaseCommitException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class UpdateFailedException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class IntegrityError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class JWTError(HTTPException):
    def __init__(self, detail: str = "An error occurred with the JSON Web Token"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class TokenExpiredError(JWTError):
    def __init__(self):
        super().__init__(detail="The provided token has expired. Please login again to obtain a new token.")

# class InvalidTokenError(JWTError):
#     def __init__(self):
#         super().__init__(detail="The provided token is invalid. Please check your token and try again.")
 
class InvalidTokenError(HTTPException):
    def __init__(self, detail: str, status_code: int = status.HTTP_401_UNAUTHORIZED):
        super().__init__(status_code=status_code, detail=detail)
        
class TokenCreationError(JWTError):
    def __init__(self, detail: str):
        super().__init__(detail=f"An error occurred while creating the token: {detail}")

# class EmailSendError(Exception): 
#     def __init__(self, detail: str): super().__init__(f"An error occurred while sending the email: {detail}")

class EmailSendError(HTTPException):
    def __init__(self, detail: str = "Failed to send email"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )