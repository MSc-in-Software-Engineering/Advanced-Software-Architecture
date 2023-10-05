import random
import time
import paho.mqtt.client as mqtt
import os

mqtt_broker = os.environ.get("MQTT_BROKER_ADDRESS", "localhost")
mqtt_port = 1883
mqtt_topic = "conveyor_belt_component"

client = mqtt.Client()
client.connect(mqtt_broker, mqtt_port, 60)
client.loop_start()

conveyor_belts_running = True

def start_conveyor_belts():
    global conveyor_belts_running
    conveyor_belts_running = True
    print("Starting all conveyor belts")

def stop_conveyor_belts():
    global conveyor_belts_running
    conveyor_belts_running = False
    print("Stopping all conveyor belts")

try:
    while True:
        if conveyor_belts_running:
            payload = "Running"
            client.publish(mqtt_topic, payload)
        else:
          payload = "Not running"
          client.publish(mqtt_topic, payload)
        time.sleep(5)  
finally:
    client.disconnect()
    client.loop_stop()


def main():
    start_conveyor_belts()