import importlib
import json
from typing import List, Callable, Type, Dict, Any, Coroutine, Awaitable, Optional
from urllib.parse import quote_plus

from keycloak import KeycloakOpenID
from memphis import Memphis, MemphisError
from memphis.message import Message
from socketio import Client

from workers import MemphisWorker, MemphisRequest, SocketIOResponse
from workers.security import Config
from workers.security.commands import GetTokenCommand
from workers.security.queries import AuthURLQuery, UserInfoQuery


class Worker(MemphisWorker):
    _sio: Client
    _keycloak: KeycloakOpenID
    _request_handlers: Dict[Type[MemphisRequest], Callable[[MemphisRequest], Coroutine[MemphisRequest, MemphisRequest, SocketIOResponse]]]

    def __init__(self, memphis: Memphis, sio: Client, keycloak: KeycloakOpenID, config: Config):
        super().__init__("security", self.consumer, memphis, config)
        self._sio = sio
        self._keycloak = keycloak
        self._request_handlers = {
            AuthURLQuery: self._auth_url_query,
            GetTokenCommand: self._code_exchange_command,
            UserInfoQuery: self._user_info_query,
        }

    @staticmethod
    def _get_type(class_name: str):
        try:
            package_name, short_name = class_name.rsplit(".", 1)
            package = importlib.import_module(package_name)
            object_type = getattr(package, short_name)
            return object_type
        except ValueError:
            return None

    @staticmethod
    def _parse_request(message_type: str, data: dict) -> MemphisRequest:
        request_type: MemphisRequest = Worker._get_type(f"workers.security.{message_type}")
        obj = request_type.model_validate(data)
        return obj

    async def _auth_url_query(self, request: AuthURLQuery) -> SocketIOResponse:
        url = self._keycloak.auth_url(request.callback_uri, request.scope)
        response = SocketIOResponse(success=True, data={"authUrl": url},
                                    recipient=request.reply_to,
                                    request_id=request.request_id)
        return response

    async def _code_exchange_command(self, request: GetTokenCommand) -> SocketIOResponse:
        try:
            token = self._keycloak.token(redirect_uri=request.callback_uri, code=quote_plus(request.code), grant_type="authorization_code")
            response = SocketIOResponse(success=True,
                                        data={
                                            "accessToken": token["access_token"],
                                            "refreshToken": token["refresh_token"]
                                        },
                                        recipient=request.reply_to,
                                        request_id=request.request_id)
        except Exception as ex:
            response = SocketIOResponse(success=False,
                                        data={
                                            "error": str(ex)
                                        },
                                        recipient=request.reply_to,
                                        request_id=request.request_id)
        return response

    async def _user_info_query(self, request: UserInfoQuery) -> SocketIOResponse:
        userinfo = self._keycloak.userinfo(request.access_token)
        response = SocketIOResponse(success=True,
                                    data={
                                        "loginName": userinfo["email"],
                                        "displayName": userinfo["name"]
                                    },
                                    recipient=request.reply_to,
                                    request_id=request.request_id)
        return response

    async def consumer(self, messages: List[Message], error: Optional[MemphisError], context: dict):
        for message in messages:
            await message.ack()
            data = json.loads(message.get_data().decode("utf-8"))
            headers = message.get_headers()
            message_type = headers.get("Request-Type")
            authorization = headers.get("Authorization")
            access_token: str | None = None
            if authorization and authorization.startswith("Bearer"):
                access_token = authorization[7:]
            request = Worker._parse_request(message_type, data)
            request.access_token = access_token
            response = await self._request_handlers[type(request)](request)
            self._sio.emit("response", data=response.model_dump_json().encode("utf-8"))
