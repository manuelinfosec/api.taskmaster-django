import uuid

import jwt
from channels.db import database_sync_to_async

from accounts.services import User
from taskmaster import env


@database_sync_to_async
def get_user(user_id: uuid.UUID):
    """
    Asynchronously retrieves a user object from the database by its ID.

    This function is decorated with `database_sync_to_async` to allow it to be used
    within synchronous code, such as Django Channels consumers, without blocking the event loop.

    Args:
        user_id (uuid.UUID): The UUID of the user to retrieve.

    Returns:
        User or None: The user object if found, or None if no user with the specified ID exists.

    Raises:
        None.
    """
    try:
        # Attempt to retrieve the user object from the database by its ID
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        # If no user with the specified ID is found, return None
        return None


class JWTAuthMiddleware:
    """
    Custom middleware that takes an JWToken from the scope header, decodes it and then
    gets the user id from the decoded JWToken then use that to get the user instance
    from the database.

    JWToken key: authorization
    """

    # header key
    jwt_key: bytes = b"authorization"

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Attempt to extract JWT token from the headers
        try:
            # Nested indexing to avoid Optional values
            token: bytes = dict(scope["headers"])[self.jwt_key]
        except KeyError:
            # If the key is not present, set the "user" in the scope to None
            scope["user"] = None

        # An else is used to retain the token in scope
        else:
            # Attempt to decode the token
            try:
                # ...using HS256 algorithm and secret key from environment
                decode_token: dict = jwt.decode(
                    jwt=token.decode(),
                    key=env.SECRET_KEY,
                    algorithms=["HS256"],
                )
            except (jwt.ExpiredSignatureError, jwt.DecodeError):
                # Any errors encountered sets the "user" in scope to None
                scope["user"] = None
            else:
                # Set "user" in the scope to user model
                scope["user"] = await get_user(decode_token["user_id"])

        # Call the next middlware or application in the stack
        return await self.app(scope, receive, send)
