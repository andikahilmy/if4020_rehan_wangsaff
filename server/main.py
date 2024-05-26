from fastapi import FastAPI,WebSocket,WebSocketDisconnect
import json
from .lib.ClientManager import ClientManager
import logging


# Setting Logging
logger = logging.getLogger('uvicorn')
logger.setLevel(logging.DEBUG)

CONNECTIONS = {}
manager = ClientManager()
app = FastAPI()

@app.get('/')
async def root():
  return {"message":"Hello World!"}



@app.websocket('/messaging')
# buat nerima pesan dari klien A dan ngirim ke klien B
async def messaging(ws:WebSocket):
  await ws.accept()
  logger.info(f"Received connection from {ws.client.host}:{ws.client.port}")
  try:
    #TODO handshake
    # data = await ws.receive_text()
    #TODO Handshake
    shared_key = ""
    manager.connect(ws,shared_key)
    # Konfirmasi handshake
    print("kirim")
    await manager.send_message(ws.client.port,"Connection Established")
    print("1")
  except WebSocketDisconnect:
    logger.info(f"Client {ws} disconnected")

  # Komunikasi
  while True:
    encrypted_message = ""
    try:
      data = await ws.receive_text()
      #TODO decrypt data dari ALS
      # Parse ke json
      message = json.loads(data)
      # Format pesan
      #{
      #  "src_port": "int",
      #  "dst_port": "int",
      #  "message": "str"
      #}
      logger.info(f"Received message from {ws}")
      #TODO encrypt data ke ALS
      encrypted_message = data
      is_success = await manager.send_message(message['dst_port'],encrypted_message)
      if is_success:
        await ws.send_text("Message sent")
      else:
        await ws.send_text("Failed to send message")
    except WebSocketDisconnect:
      logger.info(f"Client {ws} disconnected")
      break
    except json.JSONDecodeError:
      logger.error("Invalid JSON format")
      await ws.send_text(f"Failed to send message: {encrypted_message}")

@app.get("/digital-signature-param")
# buat dapatin global variabel digital signature
async def digital_signature_param():
  pass