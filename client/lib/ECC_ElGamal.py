import secrets
from .ECC import  SECP256R1,Point,ElipticCurve
import math
def generate_keypair():
  private_key = generate_privatekey()
  public_key = generate_publickey(private_key)
  return (public_key,private_key)

def generate_publickey(private_key:int)->Point:
  return  SECP256R1.get_basepoint() * private_key

def generate_privatekey()->int:
  private_key = secrets.randbelow(SECP256R1.p)
  while private_key == 0:
    private_key =  secrets.randbelow(SECP256R1.p)
  return private_key

def encode_point(plaintext:bytes)->Point: 
  #k yang digunakan adalah panjang plaintext dan 
  k = len(plaintext)
  # Jadikan plaintext sebagai integer
  m = int.from_bytes(plaintext,'little')
  # Karena p yang digunakan memenuhi p%4==3, maka apapun x nya pasti ada y
  x:int = m*k
  y = SECP256R1.y(x)
  # k disimpan di lsb m*k. k berupa int 4 byte
  x = int.from_bytes(k.to_bytes(4,'little') + x.to_bytes(math.ceil(x.bit_length() / 8),'little'),'little')
  # return titik
  return Point(x,y,SECP256R1)

def decode_point(ciphertext:Point)->bytes:
  # Tinggal bagi x dengan k
  # k tinggal di extract dari bagian belakang bytes
  k = ciphertext.x & 0xffffffff
  x = ciphertext.x >> (4*8)
  # dapatkan m
  m = x // k
  # Konversi ke bytes lagi
  plaintext = m.to_bytes(math.ceil(m.bit_length() / 8),'little')
  return plaintext

def encrypt(plaintext:bytes,public_key:Point):
  P_M:Point = encode_point(plaintext)
  k = secrets.randbelow(SECP256R1.p)
  while k == 0:
    k =  secrets.randbelow(SECP256R1.p)
  c1 = SECP256R1.get_basepoint()* k
  c2 = P_M + public_key * k
  return (c1,c2)

def decrypt(c1:Point,c2:Point,private_key:int):
  print(c1)
  print(c2)
  print("key",private_key)
  P_M =  c2 + c1*(SECP256R1.n - private_key)
  print("P_M")
  print(decode_point(P_M))
  print("AA")
  return decode_point(P_M)


#P_M + SECP256R1.get_basepoint() * private_key * k  - SECP256R1.get_basepoint()* k * private_key