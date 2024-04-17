from workers import MemphisRequest


class GetTokenCommand(MemphisRequest):
    code: str
    callback_uri: str
