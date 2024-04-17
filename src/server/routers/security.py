from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from memphis import Headers
from memphis.producer import Producer

from server.ApiUser import ApiUser
from server.dependencies import get_security_producer, get_authorization_credentials, get_current_user
from workers.security.commands import GetTokenCommand
from workers.security.queries import AuthURLQuery, UserInfoQuery

router = APIRouter()


@router.post("/login-initiated")
async def login_initiated(query: AuthURLQuery, producer: Producer = Depends(get_security_producer)):
    headers = Headers()
    headers.add("Request-Type", "queries.AuthURLQuery")
    try:
        await producer.produce(message=query.model_dump(), headers=headers, nonblocking=True)
    except Exception as ex:
        return JSONResponse({"error": str(ex)}, status_code=500)
    return JSONResponse({}, status_code=200)


@router.post("/code-received")
async def code_received(command: GetTokenCommand, producer: Producer = Depends(get_security_producer)):
    headers = Headers()
    headers.add("Request-Type", "commands.GetTokenCommand")
    try:
        await producer.produce(message=command.model_dump(), headers=headers, nonblocking=True)
    except Exception as ex:
        return JSONResponse({"error": str(ex)}, status_code=500)
    return JSONResponse({}, status_code=200)


@router.get("/token-received")
async def token_received(request_id: str, reply_to: str, producer: Producer = Depends(get_security_producer),
                         user: ApiUser = Depends(get_current_user)):
    headers = Headers()
    query = UserInfoQuery(request_id=request_id, reply_to=reply_to)
    headers.add("Request-Type", "queries.UserInfoQuery")
    headers.add("Authorization", f"Bearer {user.token}")
    try:
        await producer.produce(message=query.model_dump(), headers=headers, nonblocking=True)
    except Exception as ex:
        return JSONResponse({"error": str(ex)}, status_code=500)
    return JSONResponse({}, status_code=200)
