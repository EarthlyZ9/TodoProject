from fastapi import HTTPException, status


def raise_404_error(detail="Not found."):
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


def get_authorization_exception():
    authorization_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized."
    )
    return authorization_exception


"""
Auth Exceptions
"""


def get_user_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return credentials_exception


def invalid_authentication_exception():
    token_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token_exception_response
