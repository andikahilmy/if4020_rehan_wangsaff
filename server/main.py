# from fastapi import FastAPI

# app = FastAPI(port=args.port)

# @app.get('/')
# async def root():
#   return {"message":"Hello World!"}


# @app.post('/connect')
# # buat handshake
# async def connect():
#   pass

# @app.post('/transfer')
# # buat nerima pesan dari klien A dan ngirim ke klien B
# async def transfer():
#   pass

# @app.get("/digital-signature-param")
# # buat dapatin global variabel digital signature
# async def digital_signature_param():
#   pass

import asyncio
from websockets.server import serve
import argparse
import json

async def handler(websocket):
  async for message in websocket:
    print(message)
    request = json.loads(message)
    # Cek rutenya
    if request['route']=="connect":
      #TODO algoritma buat ALS handshake
      pass
    elif request['route']=="transfer":
      #TODO enkripsi ALS
      print(f"Sending {request['message']} to {request['server_port']}")
    elif request['route']=="digital-signature-param":
      #TODO enkripsi ALS
      pass
    else:
      await websocket.send(json.dumps)

async def main(port):
  async with serve(handler,"localhost",port):
    await asyncio.Future()


if __name__=="__main__":
  parser = argparse.ArgumentParser(description="Run Wangsaff Server")
  parser.add_argument("port", type=int, help="Port to run server")
  args = parser.parse_args()
  asyncio.run(main(args.port))
