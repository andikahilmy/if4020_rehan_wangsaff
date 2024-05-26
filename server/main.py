from fastapi import FastAPI,WebSocket,WebSocketDisconnect
import json
from .lib.ClientManager import ClientManager
import logging
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

from lib.Cipher import Cipher
import base64
import secrets
import math


# Setting Logging
logger = logging.getLogger('uvicorn')
logger.setLevel(logging.DEBUG)

CONNECTIONS = {}
manager = ClientManager()
app = FastAPI()

private_key = ec.generate_private_key(ec.SECP384R1())
public_key = private_key.public_key().public_bytes(
  encoding=serialization.Encoding.PEM,
  format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode()

@app.get('/')
async def root():
  return {"message":"Hello World!"}



@app.websocket('/messaging')
# buat nerima pesan dari klien A dan ngirim ke klien B
async def messaging(ws:WebSocket):
  await ws.accept()
  logger.info(f"Received connection from {ws.client.host}:{ws.client.port}")
  try:
    client_public_key = await ws.receive_text()
    client_public_key = serialization.load_pem_public_key(client_public_key.encode())
    
    await ws.send_text(public_key)

    shared_key = private_key.exchange(ec.ECDH(),client_public_key)
    
    public_key_bytes = client_public_key.public_bytes(
      encoding=serialization.Encoding.PEM,
      format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # cipher = Cipher(public_key_bytes[:16],'ctr')
    # key = cipher.encrypt(shared_key)[:16]
    key = shared_key[:16]

    manager.connect(ws,key)
    # manager.connect(ws,"")
    # Konfirmasi handshake
    # await manager.send_message(ws.client.port,"Connection Established")
    print("Connection Established")
  except WebSocketDisconnect:
    logger.info(f"Client {ws} disconnected")

  # Komunikasi
  while True:
    encrypted_message = ""
    try:
      encoded_data = await ws.receive_text()
      data = base64.b64decode(encoded_data)
      
      
      # decrypt data
      sender_shared_key = manager.CONNECTIONS[ws.client.port][1]
      cipher = Cipher(sender_shared_key,'ctr')
      decrypted_data = cipher.decrypt(data).decode()
      del cipher

      # Parse ke json
      # decrypted_data = data
      message = json.loads(decrypted_data)
      # Format pesan
      #{
      #  "src_port": "int",
      #  "dst_port": "int",
      #  "message": "str"
      #}
      logger.info(f"Received message from {ws}")
      # encrypt data ke ALS
      receiver_shared_key = manager.CONNECTIONS[message['dst_port']][1]
      cipher = Cipher(receiver_shared_key,'ctr')
      encrypted_message = base64.b64encode(cipher.encrypt(json.dumps(message).encode())).decode()
      del cipher 
      # encrypted_message = json.dumps(message)
      is_success = await manager.send_message(message['dst_port'],encrypted_message)
      if is_success:
        print("Message sent")
      else:
        print("Failed to send message")
    except WebSocketDisconnect:
      logger.info(f"Client {ws} disconnected")
      break
    except json.JSONDecodeError:
      logger.error("Invalid JSON format")
      print(f"Failed to send message: {encrypted_message}")

@app.get("/digital-signature-param")
# buat dapatin global variabel digital signature pake skema schnorr
async def digital_signature_param():
  # Bangkitkan nilai p dan q
  p = secrets.randbits(1024)
  q = secrets.randbits(128)
  pq_criteria = p > q and p % q == 1
  while not pq_criteria:
    p = secrets.randbits(1024)
    q = secrets.randbits(128)
    pq_criteria = p > q and p % q == 1
  # Bangkitkan nilai a
  a = secrets.randbelow(p-1) + 1
  a_criteria = pow(a, q, p) == 1
  while not a_criteria:
    a = secrets.randbelow(p-1) + 1
    a_criteria = pow(a, q, p) == 1