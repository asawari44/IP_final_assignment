import paho.mqtt.client as mqtt
import redis
import json
from datetime import datetime
import ast
import time

SECtoMSEC = 1000000
DBpub = 3

pubNumb = 3
ip3 = "192.168.56.103"

# second of delay from one location to the following
speed = 0.2

# frame n. that trigger the streaming
triggerFrame = 30

# 705 correspond to 'overtake'
maneuver = 705

broker = "localhost"
port = 1883
timelive = 60
pubName = "{}".format(pubNumb)
myTopic = 'vehicle3'

# var for redis
msgN = 1
# instance of redis
#r = redis.Redis(db=DBpub)



# define callbacks
def on_message(client, userdata, message):
    print("received message =", str(message.payload.decode("utf-8")))


def send_message(topic, message):
    global msgN
    currentTime = datetime.now()
    client.publish(topic, message)
    #mSec = currentTime.minute * 60 * SECtoMSEC + currentTime.second * SECtoMSEC + currentTime.microsecond
    #print(message, ", mSec: ", mSec)
    #r.set('{}_{}'.format(pubName, msgN), '{}'.format(mSec))
    #msgN += 1


def read_data():
    lineList = list()
    nMessage = 0

    with open("data/v3_police.txt") as f:
        for line in f:
              lines = line.split("\n")
              line = lines[0] + "_" + ip3
              if nMessage == triggerFrame:
                send_message(myTopic, "{}".format(maneuver))
                print("trigger sent...")
              else:
                send_message(myTopic, "{}".format(line))
                print(line)
              time.sleep(speed)
              nMessage += 1


def on_connect(client, userdata, flags, rc):
    print("publishing..")


client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
print("connecting to broker")
client.connect(broker, port)

# send data
read_data()
print("data sent...")

