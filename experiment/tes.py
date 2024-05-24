import asyncio
import websockets
import socket

async def hello(uri):
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.bind(('localhost', 1999))
    async with websockets.connect(uri) as websocket:
        print(websocket.local_address)
        # await websocket.send("Hello there!")
        # greeting = await websocket.recv()
        greeting = "halo"
        print(f"Received: {greeting}")
        # greeting = await websocket.recv()
        # print(f"Received: {greeting}")        

# asyncio.run(hello('ws://localhost:3000/connect'))
asyncio.run(hello('ws://localhost:9999/messaging'))