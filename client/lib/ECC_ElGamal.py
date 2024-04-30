from tinyec import registry,Point
import secrets
def generate_keypair():
  private_key = generate_privatekey()
  public_key = generate_publickey(private_key)
  return (public_key,private_key)

def generate_publickey(private_key:int)->Point:
  curve = registry.get_curve('brainpoolP256r1')
  return private_key * curve.g

def generate_privatekey()->int:
  curve = registry.get_curve('brainpoolP256r1')
  private_key =  secrets.randbelow(curve.field.n)
  while private_key == 0:
    private_key =  secrets.randbelow(curve.field.n)
  return private_key

def encode_bytes():
  pass

def decode_bytes():
  pass

def encrypt(plaintext:bytes,public_key:Point):
  P_M = encode_bytes(plaintext)
  curve = registry.get_curve('brainpoolP256r1')
  k = secrets.randbelow(curve.field.n)
  while k == 0:
    k =  secrets.randbelow(curve.field.n)
  c1 = k * curve.g
  c2 = P_M + k * public_key
  return (c1,c2)

def decrypt(ciphertext:bytes,private_key:int,c1:Point,c2:Point):
  curve = registry.get_curve('brainpoolP256r1')
  return c2 - (curve.field.n -  private_key) * c1