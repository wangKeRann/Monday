from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # GitHub OAuth 配置
    github_client_id: str
    github_client_secret: str
    github_callback_url: str
    
    # JWT 配置
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expiration: int = 86400  # 24小时
    
    # 数据库配置
    database_url: str = "sqlite:///./app.db"
    
    class Config:
        env_file = ".env"

settings = Settings() 