import jwt
import time
from typing import Dict
from decouple import config

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

def token_response(token: str):
    return {'access_token': token}

def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}

def sign_jwt(user_name: str, role: str) -> Dict[str, str]:
    payload = {
        "user_name": user_name,
        "role": role,
        "expires": time.time() + 1800
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token=token)