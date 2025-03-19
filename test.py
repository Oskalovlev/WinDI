import asyncio
from websockets import connect


async def test():
    uri = "ws://localhost:8000/ws"
    async with connect(uri) as websocket:
        await websocket.send('{"command": "echo"}')
        response = await websocket.recv()
        print(response)

asyncio.run(test())
