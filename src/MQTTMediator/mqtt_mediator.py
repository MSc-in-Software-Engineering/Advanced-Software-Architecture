from confluent_kafka import Producer
import paho.mqtt.client as mqtt
import os
import logging

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

        kafka_producer.produce(topic, key=None, value=message)
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