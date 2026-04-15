from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from app.auth import decode_access_token, get_user_id_from_token
import logging

logger = logging.getLogger(__name__)

security = HTTPBearer(auto_error=False)

class AuthMiddleware(BaseHTTPMiddleware):
  async def dispatch(self, request:Request, call_next):
    public_paths = ["/auth/register", "/auth/login", "/docs", "/openapi.json", "redoc"]

    if request.url.path in public_paths:
      return await call_next(request)

    auth_header = request.headers.get("Authorization")

    if not auth_header:
      logger.warning(f"Missing auth header for {request.url.path}")
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing authentication token",
        headers={"WWW-Authenticate":"Bearer"},
      )

    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authorization header format. Use 'Bearer <token>'",
        headers={"WWW-Authenticate": "Bearer"},
      )
    
    token = parts[1]
    user_id = get_user_id_from_token(token)

    if not user_id:
      logger.warning(f"Invalid or expired token for {request.url.path}")
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
      )
    
    request.state.user_id = user_id
    logger.info(f"Authenticated user {user_id} accessing {request.url.path}")
        
    return await call_next(request)