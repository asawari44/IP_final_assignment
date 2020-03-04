'''
ip3 = "192.168.56.102"

#lineList = list()
with open("data/v3_police.txt") as f:
  for line in f:
    lines = line.split("\n")
    line = lines[0] + "_" + ip3
    print(line)'''
'''
import math

def calc_distance(px, py, vx, vy):

  x = vx - px
  y = vy - py

  distance = math.sqrt(x ** 2 + y ** 2)
  return distance

print(calc_distance(102, 0, 3, 0))'''
