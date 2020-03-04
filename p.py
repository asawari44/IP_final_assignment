
ip3 = "192.168.56.102"

#lineList = list()
with open("data/v3_police.txt") as f:
  for line in f:
    lines = line.split("\n")
    line = lines[0] + "_" + ip3
    print(line)