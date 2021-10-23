import paho.mqtt.client as mqtt_client
import random
import time
import json

broker = 'mqtt0.bast-dev.ru'
port = 1883
topic_prefix = 'service/weather_logger'
username = 'hackathon'
password = 'Autumn2021'
client_id = f'python-mqtt-{random.randint(0, 1000)}'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):    
        if rc != 0:
           print("Failed to connect, return code %d\n", rc)
        client.subscribe('service/weather_logger/#')

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
def normalizerOfTopic(topicCheck,client):
    global normalCheckValue
    GetNormalValue(topicCheck)
    client.publish(topic_prefix+"/"+topicCheck,send_msg[topicCheck]+normalCheckValue)
    
zalupa = []
send_msg = {
        "float":'outdoor_humidity',
        "float":'outdoor_light',
        "float":'outdoor_temperature',
        "float":'soil_humidity',
        "float":'soil_temperature'
}

normalCheckValue=-1
def GetNormalValue(topicCheck):
    global normalCheckValue
    if(topicCheck=='outdoor_humidity'):
        normalCheckValue=5
    elif(topicCheck == 'outdoor_light'):
        normalCheckValue = 2
    elif(topicCheck == 'outdoor_temperature'):
        normalCheckValue = 10    
    elif(topicCheck == 'soil_humidity'):
        normalCheckValue = 5
    elif(topicCheck == 'soil_temperature'):
        normalCheckValue = 10
    else: print("error with check")
def checkNormalize(topicCheck):
    normalize_data = {
        'outdoor_humidity':50,
        'outdoor_light':1,
        'outdoor_temperature':5.8,
        'soil_humidity':86,
        'soil_temperature':7
    }
    global send_msg
    global normalCheckValue

    GetNormalValue(topicCheck)
    
    if(abs(normalize_data[topicCheck]-send_msg[topicCheck])>normalCheckValue):
        print("Нарушено состояние ",topicCheck,"на ", normalize_data[topicCheck]-send_msg[topicCheck],
        "от нормы (",normalize_data[topicCheck],")")
        return True
    return False

def on_message(client, userdata, message):
    #print('Message:', str(message.payload.decode("utf-8")))
    #zalupa.append(message.payload)
    print(message.topic,':', (message.payload))
    #print(zalupa)
    x = float(str(message.payload.decode("utf-8")))
    global send_msg
    send_msg[str(message.topic).split("/")[2]] =x 
    if(checkNormalize(str(message.topic).split("/")[2])):
        normalizerOfTopic(str(message.topic).split("/")[2],client)


def run():
    global send_msg
    send_msg ={}
    client = connect_mqtt()
    client.on_message = on_message
    #client.subscribe([('service/weather_logger/outdoor_temperature', 0), ('service/weather_logger/soil_humidity', 0),
    #                  ('service/weather_logger/soil_temperature', 0)])
    #client.subscribe('service/weather_logger/soil_humidity')
    #client.subscribe('service/weather_logger/outdoor_temperature')
    #client.subscribe('service/weather_logger/soil_temperature')
    #client.subscribe('service/weather_logger/outdoor_humidity')
    #client.subscribe('service/weather_logger/outdoor_light')
    client.loop_forever()
    #publish(client)
run()