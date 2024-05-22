class ALS():
  def __init__(self,port:int,server_port:int) -> None:
    self.port = port
    self.server_port = server_port

  def init_connection(self)->None:
    #TODO algoritma buat ALS handshake
    pass

  def send(self,message:str)->None:
    #TODO enkripsi ALS
    print(f"Sending {message} to {self.server_port}")