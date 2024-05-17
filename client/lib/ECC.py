from typing import Type
from client.lib.utils import sqrt_mod
from dataclasses import dataclass
# Kurva: # y^2 =  x^3 + ax + b  (mod p)


class Point:
    def __init__(self,x: int,y: int,curve)->None:
        self.x = x
        self.y = y
        self.curve:ElipticCurve = curve

    # Perkalian skalar dengan titik
    def __mul__(self, scalar: int):
        if self.is_infinity():
            # k.O = O
            return self.curve.INFINITY
        elif scalar == 0:
            # 0.P = O
            return self.curve.INFINITY
        else:
            is_negative = scalar < 0
            cnt = -scalar if is_negative else scalar
            res = self.curve.INFINITY
            tmp = Point(self.x, self.y, self.curve)
            while cnt:
                if cnt % 2 == 1:  # ganjil
                    res = res + tmp
                tmp = tmp + tmp
                cnt //= 2
            if is_negative:
                return -res
            else:
                return res
            
    def __iadd__(self, point):
        return self.__add__(point)
    # Penjumlahan titik pada kurva
    # m = ((yp-yq)/(xp-xq)) mod p
    # xr = (m^2 – xp – xq) mod p
    # yr = (m(xp – xr) – yp) mod p
    def __add__(self, point):
        if self.is_infinity() and not point.is_infinity():
            # O + P = P
            return Point(point.x, point.y, point.curve)
        elif not self.is_infinity() and point.is_infinity():
            # P + O = P
            return Point(self.x, self.y, self.curve)
        elif self.x == point.x:
            if self.y == point.y and self.y != 0:
                # P + P = 2P = R
                # xr = m^2 – 2xp
                # yr = m(xp – xr) – yp
                # 𝑚=𝑑𝑦/𝑑𝑥=(3𝑥_𝑝^2+𝑎)/(2𝑦_𝑝 )
                d_y = 3 * (self.x**2) + self.curve.a
                d_x = 2 * self.y
                m = d_y * pow(d_x, -1, self.curve.p)
                x_r = (m**2 - 2 * self.x) % self.curve.p
                y_r = (m * (self.x - x_r) - self.y) % self.curve.p
                return Point(x_r, y_r, self.curve)
            elif self.y == point.y and self.y == 0:
                # P + P = 2P = O
                return self.curve.INFINITY
            else:
                # P + (-P) = 0
                # return infinity
                return self.curve.INFINITY
        else:
            # 𝑚=(𝑦_𝑝−𝑦_𝑞)/(𝑥_𝑝−𝑥_𝑞 )
            # xr = m2 – xp – xq
            # yr = m(xp – xr) – yp  

            delta_y = self.y - point.y
            delta_x = self.x - point.x
            m = delta_y * pow(delta_x, -1, self.curve.p)
            xr = (m**2 - self.x - point.x) % self.curve.p
            yr = (m * (self.x - xr) - self.y) % self.curve.p
            return Point(xr, yr, self.curve)
    def __sub__(self, point):
        return self.__add__(-point)

    # Karena P+Q == Q+P
    def __radd__(self, point):
        self.__add__(point)

    def is_infinity(self) -> bool:
        return self.x == None and self.y == None

    def __neg__(self):
        # -P
        return Point(self.x, -self.y, self.curve)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self) -> str:
        return f"({self.x},{self.y})"
    
    def __eq__(self,other:Type['Point']):
        return self.x == other.x and self.y == other.y and self.curve == other.curve


# y^2 =  x^3 + ax + b  (mod p)
@dataclass
class ElipticCurve:
    a: int
    b: int
    p: int
    n: int # Jumlah titik
    B_X: int
    B_Y: int

    # Spesial value, nilai di tak terhigga
    @property
    def INFINITY(self) -> Point:
        return Point(None, None, self)


    # Mendapatkan titik Basis
    def get_basepoint(self):
        return Point(self.B_X, self.B_Y, self)
    
    # mendapatkan nilai y
    def y(self,x:int)->int:
        # y^2 =  x^3 + ax + b  (mod p)
        # y = sqrt(x^3 + ax + b  (mod p))
        y_2 = (x**3  + self.a * x + self.b)  % self.p
        return sqrt_mod(y_2,self.p)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self) -> str:
        return f"y^2 = x^3 + {self.a}x + {self.b} (mod {self.p})"


# Sumber: https://neuromancer.sk/std/secg/secp256r1#
SECP256R1 = ElipticCurve(
    0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC,
    0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B,
    0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF,
    0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551,
    0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296,
    0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5,
)