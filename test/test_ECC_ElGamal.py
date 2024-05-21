import pytest
from client.lib.ECC_ElGamal import generate_keypair,generate_publickey,generate_privatekey,encode_point,decode_point,encrypt,decrypt
from client.lib.ECC import SECP256R1,Point
import secrets

def test_generate_privatekey():
   private_key = generate_privatekey() 
   assert private_key != 0

def test_generate_publickey():
   private_key = generate_privatekey()
   public_key = generate_publickey(private_key)
   assert public_key == SECP256R1.get_basepoint() * private_key

def test_generate_keypair(mocker):
   mocker.patch('secrets.randbelow', return_value=5000)
   private_key = generate_privatekey()
   public_key = generate_publickey(private_key)
   assert generate_keypair() == (public_key,private_key)

def test_encode_encode_point():
   plaintext = b'Halo DUnya!'
   plain_point = encode_point(plaintext)
   assert type(plain_point)==Point

   replaintext = decode_point(plain_point)
   assert type(replaintext)==bytes
   assert replaintext==plaintext

def test_encrypt(mocker):
   pub,priv = generate_keypair()
   curve = pub.curve
   # mocker.patch('client.lib.ECC_ElGamal.encode_point', return_value=Point(1000,1000,curve))
   # Coba enkripsi
   public_key = generate_publickey(generate_privatekey())
   plaintext = b"hello"
   c1,c2 = encrypt(plaintext,public_key)
   assert type(c1)==Point
   assert type(c2)==Point

def test_encrypt_decrypt():
   pub,priv = generate_keypair()
   # mocker.patch('client.lib.ECC_ElGamal.encode_point', return_value=Point(1000,1000,curve))
   # mocker.patch('client.lib.ECC_ElGamal.decode_point', return_value=b"hello")
   # Coba enkripsi
   # public_key = generate_publickey(generate_privatekey())
   plaintext = b"hello"
   c1,c2 = encrypt(plaintext,pub)
   plain = decrypt(c1,c2,priv)
   assert type(plain)==bytes
   assert plain==plaintext