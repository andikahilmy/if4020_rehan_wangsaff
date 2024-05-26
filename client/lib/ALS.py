import asyncio
import websockets
import json
import base64
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

  async def start_connection(self)->None:
    # Init websocket
    self.websocket = await websockets.connect(self.uri,ping_interval=None)
    print(f"Connected to {self.uri} from local port {self.get_port()}")
    self.connected_event.set()
    # Buat task untuk kirim pesan
    # asyncio.create_task(self._send())
    # Handshake
    await self.handshake()
    # Buat thread untuk mengirim pesan
    self.receive_task = asyncio.create_task(self._receive())
    asyncio.create_task(self._send())

  async def _receive(self)->None:
    #TODO handle penerimaan pesan
    while True:
      try:
        message = await self.websocket.recv()
        self.process_message(message)
      except websockets.ConnectionClosed:
        print("Connection closed")

  async def _send(self)->None:
    # Kirim pesan
    while True:
      message = await self.queue.get()
      encrypted_message = base64.b64encode(self.__cipher.encrypt(message)).decode()
      # encrypted_message = message
      await self.websocket.send(encrypted_message)
      print(f"Sending {encrypted_message} to {self.server_port}")


  #Interface untuk kirim pesan
  async def send(self,message:str)->None:
    await self.queue.put(message.encode())

  def get_port(self)->int|None:
    if self.websocket:
      return self.websocket.local_address[1]
    return None

  def process_message(self,message:str)->None:
    encoded_data = message
    #Parse json
    if encoded_data=='Connection Established':
      self.on_message_received(encoded_data)
      return
    try:
      data = base64.b64decode(encoded_data)
      decrypted_message = self.__cipher.decrypt(data)
      message_from_json = json.loads(decrypted_message)['message']
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

  async def handshake(self) -> None:
    # Kirim public key
    await self.websocket.send(self.__public_key.decode())
    # Terima public key dari server
    server_public_key = await self.websocket.recv()
    server_public_key = serialization.load_pem_public_key(server_public_key.encode())
    # Hitung shared key
    shared_key = self.__private_key.exchange(ec.ECDH(),server_public_key)
    # Derive key
    public_key_bytes = server_public_key.public_bytes(
      encoding=serialization.Encoding.PEM,
      format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).replace(b'-----BEGIN PUBLIC KEY-----\n',b'').replace(b'\n-----END PUBLIC KEY-----\n',b'')
    if len(public_key_bytes)<16:
      # Tambahkan ke public_key_bytes sampai panjangnya 16
      ctr = 0
      while len(public_key_bytes)<16:
        public_key_bytes += ctr.to_bytes(1,'big')
        ctr+=1
    self.__key = shared_key[:16]
    self.__cipher = Cipher(self.__key, 'ctr')