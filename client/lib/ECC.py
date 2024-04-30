from dataclasses import dataclass
from typing import Type

# Kurva: # y^2 =  x^3 + ax + b  (mod p)

@dataclass
class Point():
  x:int
  y:int
  curve:ElipticCurve
  # Perkalian skalar dengan titik 
  def __mul__(self,scalar:int):
    pass

  # Penjumlahan titik pada kurva
  # m = ((yp-yq)/(xp-xq)) mod p
  # xr = (m^2 – xp – xq) mod p
  # yr = (m(xp – xr) – yp) mod p  
  def __add__(self,point:Point)->Point:
    if(self.x==point.x):
      # P + (-P) = 0
      # return infinity
      return curve.INFINITY
    delta_y = self.y-point.y
    delta_x =self.x-point.x
    m = delta_y * pow(delta_x,-1,curve.p)
    xr = (m**2 - self.x - point.x ) % curve.p
    yr = (m * (self.x-point.x) - self.y) % curve.p
    return Point(xr,yr,self.curve)

  # Karena P+Q == Q+P
  def __radd__(self,point:Point)->Point:
    self.__add__(point)

  def __is_infinity(self)->bool:
    return self.x==None and self.y == None


# y^2 =  x^3 + ax + b  (mod p)
@dataclass
class ElipticCurve():
  a:int
  b:int
  p:int
  n:int # Jumlah titik

  # Spesial value, nilai di tak terhigga
  @property
  def INFINITY(self)->Point:
    return Point(None,None,self)
  # Mendapatkan titik Basis
  def get_basepoint(self):
    pass


