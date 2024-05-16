import secrets
from client.lib.ECC import  SECP256R1,Point
def generate_keypair():
  private_key = generate_privatekey()
  public_key = generate_publickey(private_key)
  return (public_key,private_key)

def generate_publickey(private_key:int)->Point:
  return  SECP256R1.get_basepoint() * private_key

def generate_privatekey()->int:
  private_key = secrets.randbelow(SECP256R1.n)
  while private_key == 0:
    private_key =  secrets.randbelow(SECP256R1.n)
  return private_key

def encode_point()->Point:
  pass

def decode_point():
  pass

def encrypt(plaintext:bytes,public_key:Point):
  P_M:Point = encode_point(plaintext)
  k = secrets.randbelow(SECP256R1.n)
  while k == 0:
    k =  secrets.randbelow(SECP256R1.n)
  c1 = SECP256R1.get_basepoint()* k
  c2 = P_M + public_key * k
  return (c1,c2)

def decrypt(c1:Point,c2:Point,private_key:int):
  P_M =  c2 - c1 * (SECP256R1.n - private_key)
  return decode_point(P_M)