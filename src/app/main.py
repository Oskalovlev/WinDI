from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.app.exeptions.auth_exp import (
    TokenExpiredException,
    TokenNoFoundException
)
from src.app.config.app_config import app_settings
from src.app.interfaces.services.connection_manager import manager
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


# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         try:
#             data = await websocket.receive_text()
#             print(f"Received message: {data}")
#             await websocket.send_text(f"Message received: {data}")
#         except WebSocketDisconnect:
#             break


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if "type" in data and data["type"] == "personal":
                await manager.send_personal_message(
                    data["message"],
                    data["receiver_id"]
                )
            elif "type" in data and data["type"] == "group":
                await manager.broadcast(data["message"], data["group_id"])
            else:
                await websocket.send_text("Invalid message format.")
    except WebSocketDisconnect:
        manager.disconnect(websocket)


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
