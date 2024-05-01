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
    if(self.__is_infinity()):
      # k.O = O
      return self.curve.INFINITY
    elif(scalar==0):
      #0.P = O
      return self.curve.INFINITY
    else:
      is_negative = scalar<0      
      cnt = -scalar if is_negative else scalar
      res = self.curve.INFINITY
      tmp = Point(self.x,self.y,self.curve)
      while cnt:
        if cnt % 2 == 1: # ganjil
          res = res + tmp
        tmp = tmp + tmp
        cnt //= 2
      if is_negative:
        return -res
      else:
        return res

  # Penjumlahan titik pada kurva
  # m = ((yp-yq)/(xp-xq)) mod p
  # xr = (m^2 – xp – xq) mod p
  # yr = (m(xp – xr) – yp) mod p  
  def __add__(self,point:Point)->Point:
    if(self.__is_infinity() and not point.__is_infinity()):
      # O + P = P
      return Point(point.x,point.y,point.curve)
    elif (not self.__is_infinity() and point.__is_infinity()):
      # P + O = P
      return Point(self.x,self.y,self.curve)
    elif(self.x==point.x):
      if(self.y==point.y and self.y!=0):
        # P + P = 2P = R
        # xr = m^2 – 2xp
        # yr = m(xp – xr) – yp  
        # 𝑚=𝑑𝑦/𝑑𝑥=(3𝑥_𝑝^2+𝑎)/(2𝑦_𝑝 )
        d_y = 3 * (self.x ** 2) + self.curve.a
        d_x = 2 * self.y
        m = d_y * pow(d_x,-1,self.curve.p)
        x_r = m**2 - 2*self.x
        y_r = m * (self.x - x_r) - self.y
        return Point(x_r,y_r,self.curve)
      elif(self.y==point.y and self.y==0):
        # P + P = 2P = O
        return self.curve.INFINITY
      else:
        # P + (-P) = 0
        # return infinity
        return self.curve.INFINITY
    else:
      delta_y = self.y-point.y
      delta_x =self.x-point.x
      m = delta_y * pow(delta_x,-1,self.curve.p)
      xr = (m**2 - self.x - point.x ) % self.curve.p
      yr = (m * (self.x-point.x) - self.y) % self.curve.p
      return Point(xr,yr,self.curve)

  # Karena P+Q == Q+P
  def __radd__(self,point:Point)->Point:
    self.__add__(point)

  def __is_infinity(self)->bool:
    return self.x==None and self.y == None
  
  def __neg__(self)->Point:
    # -P
    return Point(self.x,-self.y,self.curve)


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


