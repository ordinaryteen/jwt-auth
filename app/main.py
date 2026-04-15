from fastapi import FastAPI
from app.routes import auth_routes, task_routes
from app.middleware.auth_middleware import AuthMiddleware

app = FastAPI(
    title="Stateless Task Manager API",
    description="""
    This API demonstrates HTTP STATELESSNESS in action.
    
    KEY CONCEPTS:
    - The server NEVER remembers you're logged in
    - You must send your JWT token on EVERY request
    - The token is cryptographically verified (no database lookup!)
    - Each request is completely self-contained
    
    HOW TO USE:
    1. POST /auth/register - Create an account
    2. POST /auth/login - Get your JWT token
    3. Copy the token
    4. For all /tasks endpoints, add header: Authorization: Bearer <your-token>
    
    NOTICE: The server doesn't store sessions. The token IS the session.
    """,
    version="1.0.0"
)

app.add_middleware(AuthMiddleware)

app.include_router(auth_routes.router)
app.include_router(task_routes.router)

@app.get("/", tags=["root"])
async def root():
    return {
        "message": "Stateless Task Manager API",
        "docs": "/docs",
        "principle": "HTTP is stateless. Every request must carry its own authentication."
    }

@app.get("/health", tags=["root"])
async def health_check():
    """Simple health check endpoint (public, no auth needed)"""
    return {"status": "healthy", "stateless": True}