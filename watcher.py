import json
import redis
import math
import paho.mqtt.client as mqtt
from datetime import datetime
import ast
broker = "localhost"
port = 1883
timelive = 60
SECtoMSEC = 1000000
DBsub = 0
# 705 corresponds to 'overtake', 100 corresponds to 'stop streaming'
overtake = "705"
stopStreaming4watcher = "100"
stopStreaming4vehicles = "101"
# radius within the vehicles can communicate
radius = 30

stream1 = False
stream2 = False


positions_1 = []
positions_2 = []
positions_3 = []

#myTopic = "vehicle1"
topic_list = ["vehicle1","vehicle2","vehicle3"]
topic_list1 = ["vehicle1s","vehicle2s","vehicle3s"]
subNumb = "watcher"
subName = "{}".format(subNumb)

dist31, dist32 = radius + 1, radius + 1

# var for redis
msgN = 0
# instance of redis
#r = redis.Redis(db=DBsub)


# define callbacks
def calc_distance(px, py, vx, vy):
    '''R = 6373.0
    lat1 = math.radians(location[0])
    lon1 = math.radians(location[1])
    lat2 = math.radians(location_v[0])
    lon2 = math.radians(location_v[1])
    #print("===================================")
    #print("lat1",lat1)
    #print("lon1",lon1)
    dlon = lon2 - lon1
    #change in coordinates

    dlat = lat2 - lat1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    #Haversine formula

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c'''
    x = vx - px
    y = vy - py

    distance = math.sqrt(x**2 + y**2)
    return distance

def on_connect(client, userdata, flags, result):
    #print("Connection : {}".format(result))
    # tu subscribe to more topic(["topic1", "topic2"])
    client.subscribe(topic_list[0])
    client.subscribe(topic_list[1])
    client.subscribe(topic_list[2])
    print("Client subscribed to: {}, {}, {}".format(topic_list[0], topic_list[1], topic_list[2]))

def send_message(topic, message):
    client.publish(topic, message)

# vars to record distance history
b31, b32 = -1, -1
dist31_nMinus1 = 100*radius + 1
dist32_nMinus1 = 100*radius + 1

def on_message(client, userdata, msg):
    global msgN, dist31, dist32, stream1, stream2, b31, b32, dist31_nMinus1, dist32_nMinus1
    #currentTime = datetime.now()
    message = str(msg.payload.decode("utf-8"))
    #print(message)
    
    # message = timeST_x_y_ip
    if message == overtake:
        stream1 = True
        stream2 = True
        print("Stream requested...")
    if message == stopStreaming4watcher:
        stream1 = False
        stream2 = False
        print("Stopping Stream...")


    if(msg.topic == topic_list[2]):
        if message == overtake:
            print("Trigger arrived.")
        elif message == stopStreaming4watcher:
            print("stopStreaming arrived.")
        else:
            positions_3.append(message)
        
            if stream1 == True or stream2 == True:
                pos3 = positions_3[-1].split("_")
                pos1 = positions_1[-1].split("_")
                pos2 = positions_2[-1].split("_")

                dist31 = calc_distance(float(pos3[1]), float(pos3[2]), float(pos1[1]), float(pos1[2]))
                dist32 = calc_distance(float(pos3[1]), float(pos3[2]), float(pos2[1]), float(pos2[2]))
                print("Police from bike: {} m. Police from car: {} m".format(round(dist31, 2), round(dist32, 2)))

                b31 = dist31 - dist31_nMinus1
                b32 = dist32 - dist32_nMinus1

                dist31_nMinus1 = dist31
                dist32_nMinus1 = dist32

                # are v1 and v3 close enough??
                if dist31 <= radius and b31 <= 0:
                    # msg = nFrame_ip
                    # to v3 we send the n. of message(frame number) and the ip addr. of v1
                    update4v3 = "{}_{}".format(msgN, pos1[3])
                    # to v1 we send the n. of message(frame number) and the ip addr. of v3
                    update4v1 = "{}_{}".format(msgN, pos3[3])
                    # start to stream from FRAME[msgN]
                    client.publish(topic_list1[2], update4v3)
                    client.publish(topic_list1[0], update4v1)
                    print("Vehicle 1 IS streaming")
                elif dist31 <= radius and b31 > 0:
                    update4v3 = "{}_{}".format(msgN, pos1[3])
                    # to v1 we send the n. of message(frame number) and the ip addr. of v3
                    update4v1 = "{}_{}".format(msgN, pos3[3])
                    # start to stream from FRAME[msgN]
                    client.publish(topic_list1[2], update4v3)
                    client.publish(topic_list1[0], update4v1)
                    print("Vehicle 1 IS streaming")
                elif dist31 > radius and b31 >= 0:
                    print("Vehicle 1 is STOPPING streaming")
                    stream1 = False
                    client.publish(topic_list1[0], stopStreaming4vehicles)

                # are v2 and v3 close enough??
                if dist32 <= radius and b32 <= 0:
                    # msg = nFrame_ip
                    # to v3 we send the n. of message(frame number) and the ip addr. of v2
                    update4v3 = "{}_{}".format(msgN, pos2[3])
                    # to v2 we send the n. of message(frame number) and the ip addr. of v3
                    update4v2 = "{}_{}".format(msgN, pos3[3])
                    client.publish(topic_list1[2], update4v3)
                    client.publish(topic_list1[1], update4v2)
                    print("Vehicle 2 IS streaming")
                elif dist32 <= radius and b32 > 0:
                    update4v3 = "{}_{}".format(msgN, pos2[3])
                    # to v2 we send the n. of message(frame number) and the ip addr. of v3
                    update4v2 = "{}_{}".format(msgN, pos3[3])
                    client.publish(topic_list1[2], update4v3)
                    client.publish(topic_list1[1], update4v2)
                    print("Vehicle 2 IS streaming")
                elif dist32 > radius and b32 >= 0:
                    print("Vehicle 2 is STOPPING streaming")
                    stream2 = False
                    client.publish(topic_list1[1], stopStreaming4vehicles)

    elif msg.topic == topic_list[1]:
        positions_2.append(message)
        '''pos = message.split("_")
        posOther = positions_3[-1].split("_")
        dist = calc_distance(pos[1], pos[2], posOther[1], posOther[2])
        print(dist)'''

    elif msg.topic == topic_list[0]:
        positions_1.append(message)
        '''pos = message.split("_")
        posOther = positions_3[-1].split("_")
        dist = calc_distance(pos[1], pos[2], posOther[1], posOther[2])
        print(dist)'''

    msgN += 1


# create client1
client = mqtt.Client(subName)


# subscribe to topic1
client.on_connect = on_connect  # call-back
# print the message published on the topic
client.on_message = on_message
# connect the client
client.connect(broker, port, timelive)
# force the subscriber to listen
client.loop_forever()

