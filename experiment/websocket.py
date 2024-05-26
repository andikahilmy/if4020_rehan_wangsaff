import tkinter
import asyncio
import threading
import websockets
from websockets import exceptions
import json
from datetime import datetime

# Starthilfe für asynkrone Funktion connect
def _asyncio_thread():
    asyncio.set_event_loop(async_loop)
    async_loop.create_task(connect())
    async_loop.run_forever()

async def connect():
    try:
        async with websockets.connect("ws://localhost:9999/messaging") as websocket:
            print(websocket.local_address[1])
            asyncio.create_task(send(websocket, "Sender"))
            while True:
                message = await websocket.recv()
                print(message)
                logger("Received", message)
    except exceptions.ConnectionClosed:
        print("Connection closed")

async def send(websocket, name):
    while True:
        message = await queue.get()
        print("pesan",message)
        await websocket.send(message)
        logger("Sent", message)

def buttonexecutor(e=None):
    msg = entry.get()
    asyncio.run_coroutine_threadsafe(messagesender(msg), async_loop)
    entry.delete(0, "end")

async def messagesender(message):
    await queue.put(message)

def logger(reason, message):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    text.configure(state="normal")
    text.insert("end", f"({current_time}) [ {reason} ] {message}\n")
    text.configure(state="disabled")

def start_connection():
    # Starte Websocket Verbindung
    threading.Thread(target=_asyncio_thread,daemon=True).start()

if __name__ == '__main__':
    # Asyncio
    async_loop = asyncio.new_event_loop()
    queue = asyncio.Queue()

    # Erstelle tkinter
    root = tkinter.Tk()
    root.title("Messenger")

    text = tkinter.Text(root, width=150, state="disabled")
    text.pack()

    entry = tkinter.Entry(root, width=100)
    entry.pack()

    tkinter.Button(master=root, text="Senden", command=buttonexecutor).pack()

    start_connection()

    # Starte tkinter
    root.mainloop()
