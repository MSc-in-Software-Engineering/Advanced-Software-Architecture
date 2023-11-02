import random
import time
import paho.mqtt.client as mqtt
import os

mqtt_broker = os.environ.get("MQTT_BROKER_ADDRESS", "localhost")
mqtt_port = 1883
mqtt_topic = "robotic_arms"

client = mqtt.Client()

client.connect(mqtt_broker, mqtt_port,60)
client.loop_start()

try:
    while True:
        client.publish(mqtt_topic, payload=str(0), qos=0)
        time.sleep(30)
        client.publish(mqtt_topic, payload=str(1), qos=0)
        time.sleep(30)
finally:
    client.disconnect()
    client.loop_stop()