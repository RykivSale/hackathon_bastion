from paho.mqtt import client as mqtt_client
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
        time.sleep(1)
        # if rc == 0:
        #    print("Connected to MQTT Broker!")
        # else:
        #    print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic_prefix, msg)
        result: [0, 1]
        status = result[0]
zalupa = []


def on_message(client, userdata, message):
    #print('Message:', str(message.payload.decode("utf-8")))
    zalupa.append(message.payload)
    print(message.topic,':', (message.payload))
    print(zalupa)


def run():
    zalupa.clear()
    client = connect_mqtt()

    client.loop_start()
    #client.subscribe([('service/weather_logger/outdoor_temperature', 0), ('service/weather_logger/soil_humidity', 0),
    #                  ('service/weather_logger/soil_temperature', 0)])
    client.subscribe('service/weather_logger/outdoor_temperature')
    client.subscribe('service/weather_logger/soil_humidity')
    client.subscribe('service/weather_logger/soil_temperature')
    client.subscribe('service/weather_logger/outdoor_humidity')
    client.subscribe('service/weather_logger/outdoor_light')
    client.on_message = on_message
    publish(client)
run()
