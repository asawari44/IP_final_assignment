import json
import redis
import paho.mqtt.client as mqtt
from datetime import datetime

broker = "localhost"
port = 1883
timelive = 60
SECtoMSEC = 1000000
DBsub = 0

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

def on_connect(client, userdata, flags, result):
    print("Connection : {}".format(result))
    # tu subscribe to more topic(["topic1", "topic2"])
    #client.subscribe(["vehicle1","vehicle2","vehicle3"])
    client.subscribe("vehicle2")
    client.subscribe("vehicle1")
    #client.subscribe[("vehicle1",0),("vehicle2",1),("vehicle3",2)]
    #print("Subscribed to: ", unlist(topic_list))

def on_message(client, userdata, msg):
    global msgN
    currentTime = datetime.now()
    message = str(msg.payload.decode("utf-8"))
    #myInfo = message.split('_')
    # myInfo[0] = pubName
    # myInfo[1] = nMessage
    # myInfo[2] = speed
    print(message.split("{")[1])
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
