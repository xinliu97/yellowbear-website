from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Optional
import httpx
import json
from os import getenv
from .. import models, database
from ..auth import create_access_token

router = APIRouter()

WECHAT_APP_ID = getenv("WECHAT_APP_ID")
WECHAT_APP_SECRET = getenv("WECHAT_APP_SECRET")
WEIBO_APP_KEY = getenv("WEIBO_APP_KEY")
WEIBO_APP_SECRET = getenv("WEIBO_APP_SECRET")
FRONTEND_URL = getenv("FRONTEND_URL")

@router.get("/api/auth/wechat")
async def wechat_login():
    """Redirect to WeChat OAuth page"""
    redirect_uri = f"{FRONTEND_URL}/api/auth/wechat/callback"
    auth_url = f"https://open.weixin.qq.com/connect/qrconnect?appid={WECHAT_APP_ID}&redirect_uri={redirect_uri}&response_type=code&scope=snsapi_login&state=STATE#wechat_redirect"
    return RedirectResponse(url=auth_url)

@router.get("/api/auth/wechat/callback")
async def wechat_callback(code: str, db: Session = Depends(database.get_db)):
    """Handle WeChat OAuth callback"""
    async with httpx.AsyncClient() as client:
        # Exchange code for access token
        token_url = f"https://api.weixin.qq.com/sns/oauth2/access_token?appid={WECHAT_APP_ID}&secret={WECHAT_APP_SECRET}&code={code}&grant_type=authorization_code"
        token_response = await client.get(token_url)
        token_data = token_response.json()
        
        if "errcode" in token_data:
            raise HTTPException(status_code=400, detail="Failed to get WeChat access token")
        
        # Get user info
        user_info_url = f"https://api.weixin.qq.com/sns/userinfo?access_token={token_data['access_token']}&openid={token_data['openid']}"
        user_info_response = await client.get(user_info_url)
        user_info = user_info_response.json()
        
        if "errcode" in user_info:
            raise HTTPException(status_code=400, detail="Failed to get WeChat user info")
        
        # Find or create user
        user = db.query(models.User).filter(models.User.email == f"{user_info['openid']}@wechat.com").first()
        if not user:
            user = models.User(
                username=user_info["nickname"],
                email=f"{user_info['openid']}@wechat.com",
                password_hash="social_login",  # Set a placeholder password
                points=0
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Create JWT token
        access_token = create_access_token(data={"sub": user.email})
        return RedirectResponse(url=f"{FRONTEND_URL}/login?token={access_token}")

@router.get("/api/auth/weibo")
async def weibo_login():
    """Redirect to Weibo OAuth page"""
    redirect_uri = f"{FRONTEND_URL}/api/auth/weibo/callback"
    auth_url = f"https://api.weibo.com/oauth2/authorize?client_id={WEIBO_APP_KEY}&response_type=code&redirect_uri={redirect_uri}"
    return RedirectResponse(url=auth_url)

@router.get("/api/auth/weibo/callback")
async def weibo_callback(code: str, db: Session = Depends(database.get_db)):
    """Handle Weibo OAuth callback"""
    async with httpx.AsyncClient() as client:
        # Exchange code for access token
        token_url = "https://api.weibo.com/oauth2/access_token"
        data = {
            "client_id": WEIBO_APP_KEY,
            "client_secret": WEIBO_APP_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": f"{FRONTEND_URL}/api/auth/weibo/callback"
        }
        token_response = await client.post(token_url, data=data)
        token_data = token_response.json()
        
        if "error" in token_data:
            raise HTTPException(status_code=400, detail="Failed to get Weibo access token")
        
        # Get user info
        user_info_url = f"https://api.weibo.com/2/users/show.json?access_token={token_data['access_token']}&uid={token_data['uid']}"
        user_info_response = await client.get(user_info_url)
        user_info = user_info_response.json()
        
        if "error" in user_info:
            raise HTTPException(status_code=400, detail="Failed to get Weibo user info")
        
        # Find or create user
        user = db.query(models.User).filter(models.User.email == f"{user_info['id']}@weibo.com").first()
        if not user:
            user = models.User(
                username=user_info["screen_name"],
                email=f"{user_info['id']}@weibo.com",
                password_hash="social_login",  # Set a placeholder password
                points=0
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Create JWT token
        access_token = create_access_token(data={"sub": user.email})
        return RedirectResponse(url=f"{FRONTEND_URL}/login?token={access_token}")
