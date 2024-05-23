import asyncio
import websockets

async def hello(uri):
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello there!")
        greeting = await websocket.recv()
        print(f"Received: {greeting}")
        greeting = await websocket.recv()
        print(f"Received: {greeting}")        

# asyncio.run(hello('ws://localhost:3000/connect'))
asyncio.run(hello('ws://localhost:3000/messaging'))