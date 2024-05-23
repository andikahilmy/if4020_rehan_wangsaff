from fastapi import WebSocket
import logging
class ClientManager():
  def __init__(self) -> None:
    self.CONNECTIONS:dict[int,tuple] = {} #Key:PORT, value:(WebSocket, shared key)
    self.logger = logging.getLogger('uvicorn')

  def connect(self,websocket:WebSocket,shared_key):
    self.CONNECTIONS[websocket.client.port] = (websocket,shared_key)

  def disconnect(self,port:int):
    del self.CONNECTIONS[port]

  async def send_message(self,dst_port,message:str):
    try:
      self.CONNECTIONS[dst_port][0].send_text(message)
    except KeyError:
      self.logger.error("Client not found")