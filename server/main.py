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


@app.websocket('/connect')
# buat handshake
async def connect(ws:WebSocket):
  await ws.accept()
  logger.info(f"Received connection from {ws.client.host}:{ws.client.port}")
  try:
    while True:
      data = await ws.receive_text()
      #TODO Handshake
      shared_key = ""
      manager.connect(ws,shared_key)
      # TODO handshake: Konfirmasi
      await ws.send_text("Connection Established")
  except WebSocketDisconnect:
    logger.info(f"Client {ws} disconnected")

@app.websocket('/messaging')
# buat nerima pesan dari klien A dan ngirim ke klien B
async def messaging(ws:WebSocket):
  await ws.accept()
  try:
    while True:
      data = await ws.receive_text()
      #TODO decrypt data
      # Parse ke json
      message = json.loads(data)
      logger.info(f"Received message: {message} from {ws}")
      #TODO kirim ke B
      await ws.send_json(message)
  except WebSocketDisconnect:
    logger.info(f"Client {ws} disconnected")

@app.get("/digital-signature-param")
# buat dapatin global variabel digital signature
async def digital_signature_param():
  pass