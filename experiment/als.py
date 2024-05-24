import asyncio
import websockets
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog

class ALS:
    def __init__(self, uri, local_port, on_message_callback):
        self.uri = uri
        self.local_port = local_port
        self.websocket = None
        self.receive_task = None
        self.on_message_callback = on_message_callback

    async def init_connection(self):
        # Create a socket and bind it to the specified local port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', self.local_port))

        # Connect to the WebSocket server using the created socket
        self.websocket = await websockets.connect(self.uri, sock=sock)
        print(f"Connected to {self.uri} from local port {self.local_port}")

        # Start the receive messages task
        self.receive_task = asyncio.create_task(self.receive_messages())

    async def send(self, message):
        if self.websocket is None:
            raise Exception("WebSocket connection is not initialized. Call init_connection first.")
        
        await self.websocket.send(message)
        print(f"Sent: {message}")

    async def receive_messages(self):
        try:
            async for message in self.websocket:
                print(f"Received: {message}")
                self.process_message(message)
        except websockets.ConnectionClosed:
            print("WebSocket connection closed.")

    def process_message(self, message):
        # Call the callback function to update the UI
        self.on_message_callback(message)

    async def close_connection(self):
        if self.websocket is not None:
            await self.websocket.close()
            print("WebSocket connection closed.")
        
        if self.receive_task is not None:
            self.receive_task.cancel()
            try:
                await self.receive_task
            except asyncio.CancelledError:
                print("Receive task cancelled.")

class ChatApp(tk.Tk):
    def __init__(self, als):
        super().__init__()
        self.als = als
        self.title("Chat App")
        self.geometry("400x500")

        self.chat_display = scrolledtext.ScrolledText(self, state='disabled')
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.entry_field = tk.Entry(self)
        self.entry_field.pack(padx=10, pady=10, fill=tk.X)
        self.entry_field.bind("<Return>", self.send_message)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def display_message(self, message):
        self.chat_display.configure(state='normal')
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.configure(state='disabled')
        self.chat_display.see(tk.END)

    def send_message(self, event=None):
        message = self.entry_field.get()
        self.entry_field.delete(0, tk.END)
        asyncio.run_coroutine_threadsafe(self.als.send(message), asyncio.get_event_loop())
        self.display_message(f"Me: {message}")

    def on_closing(self):
        asyncio.run_coroutine_threadsafe(self.als.close_connection(), asyncio.get_event_loop())
        self.destroy()

async def main():
    uri = "ws://example.com:12345"  # Replace with the actual URI of the WebSocket server
    local_port = 8765  # Replace with the desired local port

    loop = asyncio.get_event_loop()
    on_message_callback = lambda message: app.display_message(f"User B: {message}")
    als = ALS(uri, local_port, on_message_callback)

    await als.init_connection()

if __name__ == "__main__":
    # Start the asyncio event loop in a separate thread
    loop = asyncio.get_event_loop()
    threading.Thread(target=loop.run_forever, daemon=True).start()

    # Create and start the Tkinter application
    app = ChatApp(als=None)
    asyncio.run_coroutine_threadsafe(main(), loop)

    app.mainloop()
