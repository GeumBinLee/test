import asyncio
import hashlib
import inspect
import logging
import os
import socket
import sys
from datetime import datetime

from fastapi import APIRouter, FastAPI, Form, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from starlette.middleware.cors import CORSMiddleware
from youtube.router import youtube_video as youtube
from tiktok.router import tiktok_video as tiktok



app = FastAPI(
    title="sns crawling",
    description="유튜브, 틱톡 등 크롤링 or api 활용",
    version="0.0.1",
    contact={"name": "", "email": "", "phone": ""},
    terms_of_service="",  # 추후 약관 생성 시 링크 추가
    # license_info={"name" : "", "url" : ""}
    redoc_url=None,
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.add_middleware(HTTPSRedirectMiddleware) #https만 접근 가능

app.include_router(youtube)
app.include_router(tiktok)

# 유효성 검사 처리
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print("validation 핸들러")
    print(exc)
    errors = []
    for error in exc.errors():
        field = error["loc"]
        message = error["msg"].capitalize()
        errors.append({"field": field, "error": message})
    return JSONResponse(
        status_code=422,
        content={"title": "필수값 미기입 오류", "detail": errors},
    )
