from paho.mqtt import client as mqtt_client
import random
import time

broker = 'mqtt0.bast-dev.ru'
port = 1883
topic_prefix = "service/weather_logger"
username = 'hackathon'
password = 'Autumn2021'
client_id = f'python-mqtt-{random.randint(0, 1000)}'
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

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
        #if status == 0:
        #    print(f"Send `{msg}` to topic `{topic_prefix}`")
        #else:
        #    print(f"Failed to send message to topic {topic_prefix}")
        #msg_count += 1

def on_message(client,userdata,message):
    print('Message:', str(message.payload.decode("utf-8")))
def run():
    client = connect_mqtt()
    client.loop_start()
    client.subscribe('service/weather_logger/soil_humidity')
    client.on_message = on_message
    publish(client)
    time.sleep(1)

run()
