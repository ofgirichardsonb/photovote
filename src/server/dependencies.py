from __future__ import annotations
import base64
import json
import os
from typing import List, Dict
from uuid import uuid4

import requests
from authlib.jose import KeySet, jwt
from authlib.jose.errors import BadSignatureError, JoseError
from dotenv import load_dotenv
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from memphis import Memphis
from memphis.producer import Producer
from starlette.requests import Request

from server.ApiUser import ApiUser

load_dotenv(".env")
realm_url = os.getenv("LOGIN_REALM_URL")
jwks_url = f"{realm_url}/protocol/openid-connect/certs"
response = requests.get(jwks_url)
jwks = response.json()
key_set = KeySet(jwks["keys"])
_memphis: Memphis | None = None
_producers: Dict[str, Producer] = {}


def get_header_from_token(token: str):
    header, _, _ = token.split(".")
    header = base64.urlsafe_b64decode(header + "==")
    return json.loads(header)


def find_key_by_kid(keyset: KeySet, kid: str):
    for key in keyset.keys:
        if key["kid"] == kid:
            return key
    return None


def get_authorization_credentials(request: Request):
    text = request.headers.get("Authorization")
    if text and text.startswith("Bearer "):
        scheme, access_token = text.split(" ")
        if access_token:
            return HTTPAuthorizationCredentials(scheme=scheme, credentials=access_token)
    return None


def get_current_user(creds: HTTPAuthorizationCredentials = Depends(get_authorization_credentials)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    if creds:
        token = creds.credentials
        if token:
            try:
                header = get_header_from_token(token)
                key = find_key_by_kid(key_set, header["kid"])
                claims = jwt.decode(token, key)
                iss = claims.get("iss")
                if iss != os.getenv("LOGIN_REALM_URL"):
                    raise credentials_exception
                return ApiUser(claims, token)
            except (BadSignatureError, JoseError):
                raise credentials_exception
        else:
            raise credentials_exception
    raise credentials_exception


def is_logged_in(user: ApiUser = Depends(get_current_user)) -> bool:
    return user is not None


async def get_memphis() -> Memphis:
    global _memphis
    if _memphis is None:
        _memphis = Memphis()
        await _memphis.connect(
            host=os.getenv("MEMPHIS_HOST"),
            account_id=int(os.getenv("MEMPHIS_ACCOUNT_ID")),
            username=os.getenv("MEMPHIS_USERNAME"),
            password=os.getenv("MEMPHIS_PASSWORD"))
    return _memphis


async def get_producer(memphis: Memphis, name: str, stations: str | List[str]) -> Producer:
    producer_name = f'{name}-{uuid4()}'
    if _producers.get(name) is None:
        _producers[name] = await memphis.producer(producer_name=producer_name, station_name=stations)
    return _producers[name]


async def get_security_producer(memphis: Memphis = Depends(get_memphis)) -> Producer:
    return await get_producer(memphis, "security", "security")


async def get_election_producer(memphis: Memphis = Depends(get_memphis)) -> Producer:
    return await get_producer(memphis, "election", "election")
