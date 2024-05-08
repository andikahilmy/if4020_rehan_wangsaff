import secrets
from lib.ECC import  SECP256R1,Point
def generate_keypair():
  private_key = generate_privatekey()
  public_key = generate_publickey(private_key)
  return (public_key,private_key)

def generate_publickey(private_key:int)->Point:
  return private_key * SECP256R1.get_basepoint()

def generate_privatekey()->int:
  private_key = secrets.randbelow(SECP256R1.n)
  while private_key == 0:
    private_key =  secrets.randbelow(SECP256R1.n)
  return private_key

def encode_point():
  pass

def decode_point():
  pass

def encrypt(plaintext:bytes,public_key:Point):
  P_M = encode_point(plaintext)
  k = secrets.randbelow(SECP256R1.n)
  while k == 0:
    k =  secrets.randbelow(SECP256R1.n)
  c1 = k * SECP256R1.get_basepoint()
  c2 = P_M + k * public_key
  return (c1,c2)

def decrypt(c1:Point,c2:Point,private_key:int):
  P_M =  c2 - (SECP256R1.n - private_key) * c1
  return decode_point(P_M)