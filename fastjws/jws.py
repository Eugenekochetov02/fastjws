from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer
from jose import jws
from jose.exceptions import JWSError
import time
import datetime
import json


class SingJWT:
    """
    Class for creating and signing a token.
    """
    def __init__(self, private_key: str):
        self.key: str = private_key

    def __call__(self, data: dict, exp: datetime.timedelta) -> str:
        # Create xpire time.
        exp = datetime.datetime.now() + exp
        # Add expire time in payload.
        data.update({
            "exp": int(time.mktime(exp.timetuple())),

        })
        # Return token.
        return jws.sign(data, self.key, algorithm='RS256')

class AuthJWT(HTTPBearer):
    """
    Class for verify a token.
    """
    def __init__(self, public_key: str, auto_error: bool = True):
        super(AuthJWT, self).__init__(auto_error=auto_error)
        self.key: str = public_key

    async def __call__(self, request: Request) -> dict:
        # Checking if there is a token in the header.
        if "Authorization" not in request.headers:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No token."
            )
        # Dividing the token into the type and the token itself.
        token_type, token = request.headers["Authorization"].split(" ")
        # Check token type.
        if token_type != 'Bearer':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type."
            )
        # Return token.
        return self.__verify(token)

    def __verify(self, token: str) -> dict:
        """
        Token authentication.
        """
        try:
            # Token authentication and dumps in dict.
            data = json.loads(jws.verify(token, self.key, 'RS256').decode())
            # Check token expire time.
            if data["exp"] < int(time.time()):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token time has expired."
                )
            return data
        except JWSError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
