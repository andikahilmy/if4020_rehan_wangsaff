from client.lib.ECC import SECP256R1,Point
def test_from_string():
  res = Point.from_string("(100,200)",SECP256R1)
  assert type(res)==Point
  assert res.x == 100 and res.y==200 and res.curve == SECP256R1