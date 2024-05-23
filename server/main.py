from fastapi import FastAPI,WebSocket,WebSocketDisconnect
import json

CONNECTIONS = {}
# print(args.port)
app = FastAPI()

@app.get('/')
async def root():
  return {"message":"Hello World!"}


@app.websocket('/connect')
# buat handshake
async def connect():
  #TODO handshake
  pass

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
      print("Received message:",message,"from",ws)
      #TODO kirim ke B
      await ws.send_json(message)
  except WebSocketDisconnect:
    print(f"Client {ws} disconnected")

@app.get("/digital-signature-param")
# buat dapatin global variabel digital signature
async def digital_signature_param():
  pass