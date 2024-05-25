import asyncio
import websockets
import json
class ALS():
  def __init__(self,server_port:int,on_message_received,queue:asyncio.Queue) -> None:
    self.uri = f"ws://localhost:{server_port}/messaging"
    self.websocket = None
    self.receive_task = None
    self.on_message_received = on_message_received
    self.queue = queue

  async def start_connection(self)->None:
    # Init websocket
    self.websocket = await websockets.connect(self.uri,ping_interval=None)
    print(f"Connected to {self.uri} from local port {self.get_port()}")
    # Buat task untuk kirim pesan
    # asyncio.create_task(self._send())
    # Buat thread untuk mengirim pesan
    self.receive_task = asyncio.create_task(self._send())
    #TODO algoritma buat ALS handshake
    print("kena")
    #TODO handle penerimaan pesan
    while True:
      try:
        message = await self.websocket.recv()
        print("Receive",message)
        self.process_message(message)
      except websockets.ConnectionClosed:
        print("Connection closed")

  async def _send(self)->None:
    #TODO enkripsi ALS
    # Kirim pesan
    while True:
      message = await self.queue.get()
      await self.websocket.send(message)
      print(f"Sending {message} to {self.server_port}")


  #Interface untuk kirim pesan
  async def send(self,message:str)->None:
    await self.queue.put(message)

  # async def receive(self)->None:
  #   try:
  #     print("mamoru")
  #     async for message in self.websocket:
  #       print(f"Received: {message}")
  #       self.process_message(message)
  #   except websockets.ConnectionClosed:
  #     print("WebSocket connection closed.")
  #   except Exception as e:
  #     print(f"Error in receiving messages: {e}")


  def get_port(self)->int|None:
    if self.websocket:
      return self.websocket.local_address[1]
    return None

  def process_message(self,message:str)->None:
    #TODO dekripsi ALS
    data = message
    #Parse json
    if data=='Connection Established':
      self.on_message_received(data)
      return
    try:
      print("datum",data)
      message_from_json = json.loads(data)['message']
    except json.JSONDecodeError:
      print("Failed to parse JSON")
      return
    except KeyError:
      print("Invalid JSON format")
      return
    self.on_message_received(message_from_json)

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
