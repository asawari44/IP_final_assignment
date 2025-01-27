import paho.mqtt.client as mqtt
import redis
import json
from datetime import datetime
import ast
import time
SECtoMSEC = 1000000
DBpub = 0

''' modify this parameter in the script '''
pubNumb = 1
ip1 = "192.168.56.101"
# second of delay from one location to the following
speed = 0.2

broker = "localhost"
port = 1883
timelive = 60
pubName = "{}".format(pubNumb)
myTopic = 'vehicle1'
my2Topic = "vehicle1s"

# 705 correspond to 'overtake'
maneuver = "705"
stopStreaming = "101"

# var for redis
msgN = 1
# instance of redis
#r = redis.Redis(db=DBpub)



# define callbacks
def on_message(client, userdata, message):
    print("Received message =", str(message.payload.decode("utf-8")))


def send_message(topic, message):
    global msgN
    currentTime = datetime.now()
    client.publish(topic, message)
    #mSec = currentTime.minute * 60 * SECtoMSEC + currentTime.second * SECtoMSEC + currentTime.microsecond
    print("Sending ", message)
    #r.set('{}_{}'.format(pubName, msgN), '{}'.format(mSec))
    msgN += 1


def read_data():
    lineList = list()
    nMessage=0
    with open("data/v1_bike.txt") as f:
        for line in f:
            lines = line.split("\n")
            line = lines[0] + "_" + ip1
            send_message(myTopic, "{}".format(line))
            #print(line)
            time.sleep(speed)
    '''with open("data/vehicle1.json") as f:
      for line in f:
        line = ast.literal_eval(line.strip("\n"))
        line["ip"]= "192.168.56.102"
        lineList.append(line)
        #print(lineList)
        for msg in lineList:
                nMessage += 1
                #time.sleep(0.01)
                #time.sleep(0.5)
                send_message(myTopic, "[{}:{}] {}".format(pubName, nMessage, msg))'''


def on_connect(client, userdata, flags, rc):
    print("publishing..")
    client.subscribe(my2Topic)


client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
print("connecting to broker")
client.connect(broker, port)

# send data
read_data()
print("data sent...")
# force the subscriber to listen
client.loop_forever()
