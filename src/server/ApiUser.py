from typing import List

from authlib.jose import JWTClaims

NAME_CLAIM: str = "name"
EMAIL_CLAIM: str = "email"
GIVEN_NAME_CLAIM: str = "given_name"
SURNAME_CLAIM: str = "family_name"
ROLE_CLAIM: str = "roles"


class ApiUser(object):
    email: str
    display_name: str
    given_name: str
    surname: str
    roles: List[str]
    token: str

    def __init__(self, claims: JWTClaims, token: str):
        super().__init__()
        self.email = claims.get(EMAIL_CLAIM)
        self.display_name = claims.get(NAME_CLAIM)
        self.given_name = claims.get(GIVEN_NAME_CLAIM)
        self.surname = claims.get(SURNAME_CLAIM)
        self.roles = claims["realm_access"][ROLE_CLAIM] or []
        self.token = token
