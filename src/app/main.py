from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.app.services.exeptions.statuses import (
    TokenExpiredException, TokenNoFoundException
)
from src.app.services.config.app_config import app_settings
from src.app.interfaces.controllers.main_router import (
    main_router as all_routers
)

app = FastAPI(
    title=app_settings.app.APP_TITLE,
    description=app_settings.app.DESCRIPTION
)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(all_routers)

origins = ["*"]
methods = ["*"]
headers = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers,
)


@app.get("/")
async def redirect_to_auth():

    return RedirectResponse(url="/auth")


@app.exception_handler(TokenExpiredException)
async def token_expired_exception_hendler(
    request: Request, exc: HTTPException
):
    return RedirectResponse(url="/auth")


@app.exception_handler(TokenNoFoundException)
async def token_no_found_exception_hendler(
    request: Request, exc: HTTPException
):
    return RedirectResponse(url="/auth")
