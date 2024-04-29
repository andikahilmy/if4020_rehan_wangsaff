from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def root():
  return {"message":"Hello World!"}


@app.post('/connect')
# buat handshake
async def connect():
  pass

@app.post('/transfer')
# buat nerima pesan dari klien A dan ngirim ke klien B
async def transfer():
  pass