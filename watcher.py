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
positions_1 = []
positions_2 = []
positions_3 = []
dict1={}
dict2={}
#myTopic = "vehicle1"
topic_list = ["vehicle1","vehicle2","vehicle3"]
subNumb = 1
subName = "{}".format(subNumb)


# var for redis
msgN = 1
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
    x = vx - px
    y = vy - py

    distance = math.sqrt(x**2 + y**2)
    return distance


def on_connect(client, userdata, flags, result):
    print("Connection : {}".format(result))
    # tu subscribe to more topic(["topic1", "topic2"])
    #client.subscribe(["vehicle1","vehicle2","vehicle3"])
    client.subscribe(topic_list[0])
    client.subscribe(topic_list[1])
    client.subscribe(topic_list[2])
    print("Client subscribed to: {}, {}, {}".format(topic_list[0], topic_list[1], topic_list[2]))


def on_message(client, userdata, msg):
    global msgN
    currentTime = datetime.now()
    message = str(msg.payload.decode("utf-8"))

    '''
    message_pub=message.split("{")[0]
    message_details="{"+message.split("{")[1]'''
    # message = timeST_x_y_ip

    if(msg.topic == topic_list[0]):
        positions_1.append(message)
        #a=ast.literal_eval(message_details)
        #location_v=a["location"]
        #location = ast.literal_eval(message_details_2[-1])["location"]
        pos = message.split("_")
        posOther = positions_3[-1].split("_")
        dist = calc_distance(pos[1], pos[2], posOther[1], posOther[2])
        print(dist)

        
    elif(msg.topic == topic_list[1]):
        positions_2.append(message)
        pos = message.split("_")
        posOther = positions_3[-1].split("_")
        dist = calc_distance(pos[1], pos[2], posOther[1], posOther[2])
        print(dist)

    elif(msg.topic == topic_list[2]):
        positions_3.append(message)
        pos = message.split("_")
        posOther = positions_3[-1].split("_")
        dist = calc_distance(pos[1], pos[2], posOther[1], posOther[2])
        print(dist)

    
    #[1:2041] {'ip': '192.168.56.103', 'video_ts': 4629, 'world_ts': 1582307195. 3292122, 'location': [7.691190719604492, -48.50749588012695]}
    #print('{}_{}_{}'.format(myInfo[0], myInfo[1], message))
    mSec = currentTime.minute * 60 * SECtoMSEC + currentTime.second * SECtoMSEC + currentTime.microsecond
    
    #r.set('{}_{}_{}_{}'.format(myInfo[0], myInfo[1], message), '{}'.format(mSec))
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

