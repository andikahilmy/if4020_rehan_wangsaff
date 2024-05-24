import asyncio
import websockets
class ALS():
  def __init__(self,server_port:int,on_message_received) -> None:
    self.uri = f"ws://localhost:{server_port}/messaging"
    self.websocket = None
    self.receive_task = None
    self.on_message_received = on_message_received

  async def init_connection(self)->None:
    # Init websocket
    self.websocket = await websockets.connect(self.uri)
    print(f"Connected to {self.uri} from local port {self.get_port()}")
    # Buat thread untuk menerima pesan
    self.receive_task = asyncio.create_task(self.receive())
    #TODO algoritma buat ALS handshake

  async def send(self,message:str)->None:
    #TODO enkripsi ALS
    # Kirim pesan
    if self.websocket:
      await self.websocket.send(message)
    print(f"Sending {message} to {self.server_port}")

  async def receive(self)->None:
    try:
      async for message in self.websocket:
        print(f"Received: {message}")
        self.process_message(message)
    except websockets.ConnectionClosed:
      print("WebSocket connection closed.")

  def get_port(self)->int|None:
    if self.websocket:
      return self.websocket.local_address[1]
    return None

  def process_message(self,message:str)->None:
    self.on_message_received(message)

  async def close_connection(self)->None:
    # Tutup koneksi
    if self.websocket:
      await self.websocket.close()
      print("WebSocket connection closed.")
    # Tutup thread
    if self.receive_task:
      self.receive_task.cancel()
      try:
        await self.receive_task
      except asyncio.CancelledError:
        print("Receive task cancelled.")

