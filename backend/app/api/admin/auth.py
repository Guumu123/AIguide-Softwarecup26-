from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas.admin import AdminLoginRequest, Token
from datetime import timedelta
from app.config import settings
from app.core.security import create_access_token

router = APIRouter()

@router.post('/login', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # 简单的硬编码登录示例
    if form_data.username == "admin" and form_data.password == "admin123":
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": form_data.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
