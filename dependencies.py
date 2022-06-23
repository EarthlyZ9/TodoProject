from fastapi import HTTPException, status

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


def token_exception():
    token_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token_exception_response


"""
Todos Exceptions
"""


def raise_404_error(detail="Todo not found."):
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


def get_todo_authorization_exception():
    authorization_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized."
    )
    return authorization_exception
