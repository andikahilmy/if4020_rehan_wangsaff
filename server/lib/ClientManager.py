from fastapi import WebSocket
class ClientManager():
  def __init__(self) -> None:
    self.CONNECTIONS:dict[int,tuple] = {} #Key:PORT, value:(WebSocket, shared key)

  async def connect(self,port:int,websocket:WebSocket,shared_key):
    self.CONNECTIONS[port] = (websocket,shared_key)

  async def disconnect(self,port:int):
    del self.CONNECTIONS[port]

  async def send_message(self,dst_port,message:str):
    self.CONNECTIONS[dst_port][0].send_text(message)