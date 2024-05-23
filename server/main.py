# import asyncio
# from websockets.server import serve
# import argparse
# import json

# async def handler(websocket):
#   async for message in websocket:
#     print(message)
#     request = json.loads(message)
#     # Cek rutenya
#     if request['route']=="connect":
#       #TODO algoritma buat ALS handshake
#       pass
#     elif request['route']=="transfer":
#       #TODO enkripsi ALS
#       print(f"Sending {request['message']} to {request['server_port']}")
#     elif request['route']=="digital-signature-param":
#       #TODO enkripsi ALS
#       pass
#     else:
#       await websocket.send(json.dumps)

# async def main(port):
#   async with serve(handler,"localhost",port):
#     await asyncio.Future()


# if __name__=="__main__":
#   parser = argparse.ArgumentParser(description="Run Wangsaff Server")
#   parser.add_argument("port", type=int, help="Port to run server")
#   args = parser.parse_args()
#   asyncio.run(main(args.port))


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