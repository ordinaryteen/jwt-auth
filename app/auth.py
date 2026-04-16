import os
from dotenv import load_dotenv
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext 
from typing import Optional

load_dotenv()
secret_key=os.getenv("SECRET_KEY")
algorithm=os.getenv("ALGORITHM")
access_token_minutes=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password:str, hashed_password:str) -> bool:
  pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
  return pwd_context.hash(password)

def create_access_token(data:dict, expires_delta: Optional[timedelta] = None) -> str:
  to_encode = data.copy()
  if expires_data:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=access_token_minutes)

  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
  
  return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
  try:
    payload = jwt.decode(token, secret_key, algorithms=[algorithm])
    return payload
  except JWTerror:
    return None

def get_user_id_from_token(token: str) -> Optional[int]:
  payload = decode_access_token(token)
  if payload:
    user_id = payload.get("sub")
    if user_id:
      return int(user_id)
  return None