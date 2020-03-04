from datetime import datetime

datetime.now(tz=None)
dateTimeObj = datetime.now()
nf1 = 411
nf2 = 411
nf3 = 311

carStep = (18000/410)/100
bikeStep = (10250/410)/100

''' Vehicle 1 - BIKE '''
f= open("v1_bike.txt","w+")
x, y = 0, 0
for i in range(nf1):
     x = x + bikeStep
     # timeST_x_y
     print("{}_{}_{}".format(i, x, y), file=f)
     #f.write("{}_{}_{}\n".format(i, x, y))
f.close()


''' Vehicle 3 - POLICE '''
x, y = 0, 0
f= open("v3_police.txt","w+")
# timeST_lon_lat

for i in range(nf2):
     x = x + bikeStep
     # timeST_x_y
     #f.write("{}_{}_{}\n".format(i, x, y))
     print("{}_{}_{}".format(i, x, y), file=f)
f.close()


''' Vehicle 2 - CAR '''
x, y = 180, 0
f= open("v2_car.txt","w+")
# timeST_lon_lat

for i in range(nf3):
     x = x - bikeStep
     # timeST_x_y
     #f.write("{}_{}_{}\n".format(i, x, y))
     print("{}_{}_{}".format(i, x, y), file=f)
f.close()