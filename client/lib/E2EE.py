from . import ECC_ElGamal as eg
class E2EE():
  def __init__(self) -> None:
    pass

  def encrypt(self, message:bytes, pubkey:str)->str:
    c1,c2 =  eg.encrypt(message,pubkey)
    return f"{str(c1)};{str(c2)}"

  def decrypt(self, ciphertext:str, privkey:str)->str:
    tmp = ciphertext.split(";")
    if len(tmp)<2:
      return "[UNDECIPHERABLE]"
    c1 = tmp[0]
    c2 = tmp[1]
    plaintext = eg.decrypt(c1,c2,privkey)
    return plaintext.decode('utf-8')