from typing import Any, Dict
import hmac

from starter_code.models.user import UserModel


def authenticate(username: str, password: str) -> Any:
    """Function that gets called when a user calls the /auth endpoint
    with their username and password.

    Args:
        username (str): User's userneame in string format.
        password (str): User's un-encripted password in string format.

    Returns:
        Any: A UserModel object if authentication was successful, None otherwise.
    """
    user: Any = UserModel.find_by_username(username)
    if user and hmac.compare_digest(user.password, password):
        return user


def identity(payload: Dict[str, Any]) -> int:
    """Function that gets called when user has already authenticated,
    and Flask-JWT verified their authorization header is correct.

    Args:
        payload (dict[str, Any]): A dictionary with 'identity' key, 
        which is the user is.

    Returns:
        Any: A UserModel object
    """
    user_id: int = payload['identity']
    return UserModel.find_by_id(user_id)
