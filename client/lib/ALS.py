import asyncio
import websockets
import json
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

from lib.Cipher import Cipher

class ALS():
  def __init__(self,server_port:int,on_message_received,queue:asyncio.Queue) -> None:
    self.server_port = server_port
    self.uri = f"ws://localhost:{self.server_port}/messaging"
    self.websocket = None
    self.receive_task = None
    self.on_message_received = on_message_received
    self.queue = queue
    self.connected_event = asyncio.Event()

    self.__private_key = ec.generate_private_key(ec.SECP384R1())
    self.__public_key = self.__private_key.public_key().public_bytes(
      encoding=serialization.Encoding.PEM,
      format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    self.__key = None
    self.__cipher = Cipher(self.__key, 'ctr')

  async def start_connection(self)->None:
    # Init websocket
    self.websocket = await websockets.connect(self.uri,ping_interval=None)
    print(f"Connected to {self.uri} from local port {self.get_port()}")
    self.connected_event.set()
    # Buat task untuk kirim pesan
    # asyncio.create_task(self._send())
    # Buat thread untuk mengirim pesan
    self.receive_task = asyncio.create_task(self._receive())
    asyncio.create_task(self._send())
    # Handshake
    await self.handshake()
    print("kena")

  async def _receive(self)->None:
    #TODO handle penerimaan pesan
    while True:
      try:
        message = await self.websocket.recv()
        print("Receive",message)
        self.process_message(message)
      except websockets.ConnectionClosed:
        print("Connection closed")

  async def _send(self)->None:
    # Kirim pesan
    while True:
      message = await self.queue.get()
      encrypted_message = self.__cipher.encrypt(message)
      await self.websocket.send(encrypted_message)
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
    print("socket")
    print(self.websocket.local_address)
    print("as")
    if self.websocket:
      return self.websocket.local_address[1]
    return None

  def process_message(self,message:str)->None:
    data = message
    #Parse json
    if data=='Connection Established':
      self.on_message_received(data)
      return
    try:
      print("datum",data)
      message_from_json = json.loads(data)['message']
      decrypted_message = self.__cipher.decrypt(message_from_json)
      print("Decrypted message:",decrypted_message)
    except json.JSONDecodeError:
      print("Failed to parse JSON")
      print("Data:",data)
      return
    except KeyError:
      print("Invalid JSON format")
      return
    self.on_message_received(decrypted_message)

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

  async def handshake(self) -> None:
    # Kirim public key
    await self.websocket.send(self.__public_key.decode())
    # Terima public key dari server
    server_public_key = await self.websocket.recv()
    server_public_key = serialization.load_pem_public_key(server_public_key.encode())
    # Hitung shared key
    shared_key = self.__private_key.exchange(ec.ECDH(),server_public_key)
    # Derive key
    key_derivation_cipher = Cipher(server_public_key, 'ctr')
    self.__key = key_derivation_cipher.encrypt(shared_key)
    print("Shared key:",self.__key)
    return