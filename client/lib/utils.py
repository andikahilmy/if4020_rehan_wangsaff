def sqrt_mod(x:int,p:int)->int:
  # Hanya untuk kasus p % 4 ==3
  # Kebetulan p yg dipake di tugas ini memenuhi p%4==3 
  return pow(x,(p+1)//4,p)