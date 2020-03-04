import paho.mqtt.client as mqtt
import redis
import json
from datetime import datetime
import ast
import time
SECtoMSEC = 1000000
DBpub = 3

pubNumb = 3
ip3 = "192.168.56.102"

broker = "localhost"
port = 1883
timelive = 60
pubName = "{}".format(pubNumb)
myTopic = 'vehicle3'

# var for redis
msgN = 1
# instance of redis
r = redis.Redis(db=DBpub)

# define callbacks
def on_message(client, userdata, message):
    print("received message =", str(message.payload.decode("utf-8")))


def on_log(client, userdata, level, buf):
    print("log: ", buf)


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
            print(line)


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

'''
# save record in a file
# open w/ automatic closure, tutorial: https://stackabuse.com/saving-text-json-and-csv-to-a-file-in-python/
with open(pubName + 'Records.json', 'w') as myFile:
    json.dump(record, myFile)
'''
