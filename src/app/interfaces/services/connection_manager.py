from typing import Dict, Set

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.groups: Dict[str, Set[str]] = {}

    async def connect(
        self,
        websocket: WebSocket,
        user_id: str,
        group_id: str = None
    ):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        if group_id:
            if group_id not in self.groups:
                self.groups[group_id] = set()
            self.groups[group_id].add(user_id)

    def disconnect(
        self,
        user_id: str,
        group_id: str = None
    ):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        if group_id and group_id in self.groups:
            self.groups[group_id].discard(user_id)

    async def send_personal_message(
        self,
        message: str,
        receiver_id: str
    ):
        if receiver_id in self.active_connections:
            await self.active_connections[receiver_id].send_text(message)

    async def broadcast(
        self,
        message: str,
        group_id: str
    ):
        if group_id in self.groups:
            for user_id in self.groups[group_id]:
                if user_id in self.active_connections:
                    await self.active_connections[user_id].send_text(message)


manager = ConnectionManager()
