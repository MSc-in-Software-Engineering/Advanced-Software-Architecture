import random
import time
import paho.mqtt.client as mqtt
import os

mqtt_broker = os.environ.get("MQTT_BROKER_ADDRESS", "localhost")
mqtt_port = 1883
mqtt_topic = "size_component"

def generate_random_size():
    size = random.choice(["small", "medium", "large"])
    return {"size": size}

client = mqtt.Client()

client.connect(mqtt_broker, mqtt_port, 60)
client.loop_start()

try:
    while True:
        random_size= generate_random_size()
        payload = f"Size: {random_size['size']}"
        client.publish(mqtt_topic, payload)
        time.sleep(5)  
finally:
    client.disconnect()
    client.loop_stop()