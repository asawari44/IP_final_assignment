import paho.mqtt.client as mqtt
import redis
import json
from datetime import datetime
import ast
SECtoMSEC = 1000000
DBpub = 0

''' modify this parameter in the script '''
pubNumb = 1

broker = "localhost"
port = 1883
timelive = 60
pubName = "{}".format(pubNumb)
myTopic = 'vehicle1'

# var for redis
msgN = 1
# instance of redis
r = redis.Redis(db=DBpub)

'''
# record of timestamp
record = {}
'''

# define callbacks
def on_message(client, userdata, message):
    print("received message =", str(message.payload.decode("utf-8")))


def on_log(client, userdata, level, buf):
    print("log: ", buf)


def send_message(topic, message):
    global msgN
    currentTime = datetime.now()
    client.publish(topic, message)
    mSec = currentTime.minute * 60 * SECtoMSEC + currentTime.second * SECtoMSEC + currentTime.microsecond
    print(message, ", mSec: ", mSec)
    r.set('{}_{}'.format(pubName, msgN), '{}'.format(mSec))
    msgN += 1


def read_data():
    lineList = list()
    nMessage=0
    with open("data/vehicle1.json") as f:
      for line in f:
        line = ast.literal_eval(line.strip("\n"))
        line["ip"]= "192.168.56.103"
        lineList.append(line)
        #print(lineList)
        for msg in lineList:
                nMessage += 1
                #time.sleep(0.01)
                send_message(myTopic, "[{}:{}] {}".format(pubName, nMessage, msg))


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
