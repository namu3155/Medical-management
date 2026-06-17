from jose import jwt
SECRET = "secretkey"

def create_token(data: dict):
    return jwt.encode(data, SECRET, algorithm="HS256")

def verify_token(token: str):
    return jwt.decode(token, SECRET, algorithms=["HS256"])