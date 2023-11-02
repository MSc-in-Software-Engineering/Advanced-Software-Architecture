from confluent_kafka import Producer
import paho.mqtt.client as mqtt
import os
import logging
import json

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("MQTT Mediator")


kafka_broker = os.environ.get("KAFKA_BROKER_ADDRESS")
kafka_producer = Producer({"bootstrap.servers": kafka_broker})

mqtt_broker = os.environ.get("MQTT_BROKER_ADDRESS", "localhost")
mqtt_port = 1883


def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        message = msg.payload.decode("utf-8")
        logger.info(f"Received MQTT message on topic {topic}: {message}")
        json_data = json.loads(message)
        timestamp = json_data.get("timestamp")
        message_content = json_data.get("message")

        if (topic == "robotic_arms"):
            topic = "production-cycle"
            if (message_content == "0"):
                message_content = "Taking materials from warehouse"
            else:
                message_content = "Adding package to warehouse"

        kafka_producer.produce(topic, key=None, value=json.dumps({"timestamp": timestamp, "value":message_content}))
        kafka_producer.flush()
    except Exception as e:
        logger.info(f"Error processing MQTT message: {str(e)}")


client = mqtt.Client()
client.on_message = on_message

client.connect(mqtt_broker, mqtt_port, 60)

client.subscribe("#")

client.loop_start()

try:
    while True:
        pass
except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()
finally:
    client.disconnect()
    client.loop_stop()
