"""Auth API endpoints — register, login, me."""
import os
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.services.auth_service import auth_service

router = APIRouter()


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = ""
    plan: Optional[str] = "starter"


class LoginRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    success: bool
    token: Optional[str] = None
    user: Optional[dict] = None
    error: Optional[str] = None


@router.post("/auth/register", response_model=AuthResponse)
async def register(request: RegisterRequest):
    """Register a new user account."""
    if not request.email or "@" not in request.email:
        raise HTTPException(status_code=400, detail="Invalid email address")
    if len(request.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    result = auth_service.register(
        email=request.email,
        password=request.password,
        name=request.name or "",
        plan=request.plan or "starter",
    )
    if not result["success"]:
        raise HTTPException(status_code=409, detail=result.get("error", "Registration failed"))
    return result


@router.post("/auth/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    """Authenticate and receive a JWT token."""
    result = auth_service.login(email=request.email, password=request.password)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result.get("error", "Authentication failed"))
    return result


@router.get("/auth/me")
async def get_me(authorization: Optional[str] = Header(None)):
    """Get current authenticated user info."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")

    token = authorization.split(" ", 1)[1]
    user = auth_service.verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user


@router.post("/auth/logout")
async def logout():
    """Logout (client-side: discard token)."""
    return {"success": True, "message": "Logged out successfully"}
