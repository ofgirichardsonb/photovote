from workers.MemphisRequest import MemphisRequest


class AuthURLQuery(MemphisRequest):
    callback_uri: str
    scope: str
