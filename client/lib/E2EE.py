from . import ECC_ElGamal as eg
from .ECC import Point,SECP256R1
class E2EE():
  def __init__(self) -> None:
    pass

  @staticmethod
  def encrypt(message:bytes, pubkey:str)->str:
    c1,c2 =  eg.encrypt(message,Point.from_string(pubkey,SECP256R1))
    return f"{str(c1)};{str(c2)}"

  @staticmethod
  def decrypt(ciphertext:str, privkey:str)->str:
    tmp = ciphertext.split(";")
    print("tmp",tmp)
    if len(tmp)<2:
      return "[UNDECIPHERABLE]"
    c1 = tmp[0]
    c2 = tmp[1]
    print(privkey,type(privkey))
    plaintext = eg.decrypt(Point.from_string(c1,SECP256R1),Point.from_string(c2,SECP256R1),int(privkey))
    return plaintext.decode('utf-8')