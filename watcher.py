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
maneuver = "705"
stopStreaming = "100"
# radius within the vehicles can communicate
radius = 20

stream = False

v1s = False
v2s = False

positions_1 = []
positions_2 = []
positions_3 = []
dict1={}
dict2={}
#myTopic = "vehicle1"
topic_list = ["vehicle1","vehicle2","vehicle3"]
subNumb = "watcher"
subName = "{}".format(subNumb)

dist31, dist32 = -1, -1

# var for redis
msgN = 0
# instance of redis
r = redis.Redis(db=DBsub)

'''
print("db1 size: {}".format(r.dbsize()))
r.flushdb()
print("db1 size: {} after flushdb()".format(r.dbsize()))
'''
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
    print("calc func")
    x = vx - px
    y = vy - py

    distance = math.sqrt(x**2 + y**2)
    print(distance)
    return distance


def on_connect(client, userdata, flags, result):
    #print("Connection : {}".format(result))
    # tu subscribe to more topic(["topic1", "topic2"])
    #client.subscribe(["vehicle1","vehicle2","vehicle3"])
    client.subscribe(topic_list[0])
    client.subscribe(topic_list[1])
    client.subscribe(topic_list[2])
    #print("Client subscribed to: {}, {}, {}".format(topic_list[0], topic_list[1], topic_list[2]))

def send_message(topic, message):
    client.publish(topic, message)


def on_message(client, userdata, msg):
    global msgN, dist31, dist32, stream
    currentTime = datetime.now()
    message = str(msg.payload.decode("utf-8"))
    #print(message)
    
    # message = timeST_x_y_ip
    if message == maneuver:
        stream = True
        print("stream required")
    if message == stopStreaming:
        stream = False 


    if(msg.topic == topic_list[2]):
        positions_3.append(message)
        #a=ast.literal_eval(message_details)
        #location_v=a["location"]
        #location = ast.literal_eval(message_details_2[-1])["location"]
        
        if stream == True:
            pos3 = positions_3[-1].split("_")
            pos1 = positions_1[-1].split("_")
            pos2 = positions_2[-1].split("_")

            dist31 = calc_distance(float(pos3[1]), float(pos3[2]), float(pos1[1]), float(pos1[2]))
            dist32 = calc_distance(float(pos3[1]), float(pos3[2]), float(pos2[1]), float(pos2[2]))
            print("Distance of police(v3) from bike(v1): {}. Distance of police from car(v2): {}".format(dist31, dist32))

            # are v1 and v3 close enough??
            if dist31 <= radius:
                v1s = True
                # msg = nFrame_ip
                # to v3 we send the n. of message(frame number) and the ip addr. of v1
                update4v3 = "{}_{}".format(msgN, pos1[3])
                # to v1 we send the n. of message(frame number) and the ip addr. of v3
                update4v1 = "{}_{}".format(msgN, pos3[3])
                client.publish(topic_list[2], update4v3)
                client.publish(topic_list[0], update4v1)
                print("Vehicle 1 start stram")
            elif dist31 > radius and v1s:
                stream = False
                client.publish(topic_list[0], stopStreaming)                 

            # are v2 and v3 close enough??
            if dist32 <= radius:
                v2s = True
                # msg = nFrame_ip
                # to v3 we send the n. of message(frame number) and the ip addr. of v2
                update4v3 = "{}_{}".format(msgN, pos2[3])
                # to v2 we send the n. of message(frame number) and the ip addr. of v3
                update4v2 = "{}_{}".format(msgN, pos3[3])
                client.publish(topic_list[2], update4v3)
                client.publish(topic_list[1], update4v2)
                print("Vehicle 2 start stream")
            elif dist32 > radius and v2s:
                stream = False
                client.publish(topic_list[1], stopStreaming)
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

