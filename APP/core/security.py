from    datetime import datetime, timedelta, timezone
from authlib.jose import JoseError, jwt
from fastapi import HTTPException
from config import settings

ALGOR=settings.JWT_ALGORITHM
SEC_KEY=settings.JWT_SECRET_KEY
ACCESS_TOKEN_EXPIRY_MINUTES=30


def create_access_token(data:dict):
    header={'algo':ALGOR}
    expire=datetime.now(timezone.utc) + timedelta(ACCESS_TOKEN_EXPIRY_MINUTES)
    payload=data.copy()
    payload.update({'exp':expire})
    return jwt.encode(header,payload,SEC_KEY).decode('utf-8')


def verify_access_token(token:str):
    try:
        claim=jwt.decode(token,SEC_KEY,ALGOR)
        return claim
    except JoseError:
        raise HTTPException(status_code=401,detail="Invalid Token")