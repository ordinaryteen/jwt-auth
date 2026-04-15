from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserRegister(BaseModel):
  email: EmailStr
  password: str
  name: str

class UserLogin(BaseModel):
  email: EmailStr
  password: str

class TokenResponse(BaseModel):
  access_token: str
  token_type: str = "bearer"
  expires_in: int

### 

class TaskCreate(BaseModel):
  title: str
  description: Optional[str] = None

class TaskUpdate(BaseModel):
  title: Optional[str] = None
  description: Optional[str] = None
  completed: Optional[bool] = None

class TaskResponse(BaseModel):
  id: int
  title: str
  description: Optional[str]
  completed: bool
  user_id: int
  created_at: datetime
  updated_at: datetime

class UserResponse(BaseModel):
  id: int
  email: str
  name: str