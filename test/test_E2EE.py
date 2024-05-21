from client.lib.E2EE import E2EE
from client.lib.ECC_ElGamal import generate_keypair
import pytest
import re

@pytest.fixture
def key_pair():
  return generate_keypair()

def test_encrypt(key_pair):
  ciphertext = E2EE.encrypt(b"hello",str(key_pair[0]))
  assert type(ciphertext)==str
  assert re.match(r"\([0-9]+,[0-9]+\);\([0-9]+,[0-9]+\)",ciphertext)

def test_encrypt_decrypt(key_pair):
  plaintext = E2EE.decrypt(E2EE.encrypt(b"hello",str(key_pair[0])),str(key_pair[1]))
  assert type(plaintext)==str
  assert plaintext=="hello"