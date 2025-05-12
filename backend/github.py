import httpx
from fastapi import HTTPException
from config import settings

async def get_github_access_token(code: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": settings.github_client_id,
                "client_secret": settings.github_client_secret,
                "code": code,
            },
            headers={"Accept": "application/json"},
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="获取GitHub访问令牌失败")
        
        data = response.json()
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error_description"])
        
        return data["access_token"]

async def get_github_user_info(access_token: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"token {access_token}",
                "Accept": "application/json",
            },
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="获取GitHub用户信息失败")
        
        user_data = response.json()
        
        # 获取用户邮箱
        email_response = await client.get(
            "https://api.github.com/user/emails",
            headers={
                "Authorization": f"token {access_token}",
                "Accept": "application/json",
            },
        )
        
        if email_response.status_code == 200:
            emails = email_response.json()
            primary_email = next((email["email"] for email in emails if email["primary"]), None)
        else:
            primary_email = None
        
        return {
            "github_id": str(user_data["id"]),
            "username": user_data["login"],
            "email": primary_email or user_data.get("email"),
            "avatar": user_data["avatar_url"],
        } 