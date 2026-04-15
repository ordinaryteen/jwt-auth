from fastapi import APIRouter, HTTPException, status
from app.models import UserRegister, UserLogin, TokenResponse, UserResponse
from app.database import db
from app.auth import verify_password, get_password_hash, create_access_token
from datetime import timedelta 

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserRegister, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
  existing_user = db.get_user_by_email(user_data.email)
  if existing_user:
    raise HTTPException(
      status_code=status.HTTP_409_CONFLICT,
      detail="User with this email already exists"
    )
  
  hashed_password = get_password_hash(user_data.password)

  user = db.create_user(
    email=user_data.email,
    password_hash=hashed_password,
    name=user_data.name
  )

  return UserResponse(
    id=user["id"],
    email=user["email"],
    name=user["name"]
  )

@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
  user = db.get_user_by_email(credentials.email)
  if not user:
      raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Invalid email or password"
      )
  
  if not verify_password(credentials.password, user["password_hash"]):
      raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Invalid email or password"
      )
  
  access_token = create_access_token(data={"sub": str(user["id"])})
  
  return TokenResponse(
      access_token=access_token,
      token_type="bearer",
      expires_in=30 * 60  
  )

