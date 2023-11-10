"""Storing finished goods, Manage inventory levels, Stores safely and efficiently """

import logging
import os
import random
import psycopg2
import json
import datetime
from time import sleep
import paho.mqtt.client as mqtt
import threading

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("MQTTWarehouse")

postgres_connection = psycopg2.connect(
    database="supplychainmanagement",
    user="postgres",
    password="admin",
    host="supply-chain-management-database",
    port="5432",
)
connection_cursor = postgres_connection.cursor()

mqtt_broker = os.environ.get("MQTT_BROKER_ADDRESS", "localhost")
mqtt_port = 1883
    
def on_message(client, userdata, msg):
    try:
        if len(buckets) != 0:
            produce_bucket_notification()
            logger.info(f"Warehouse has [{len(buckets)}] bucket(s) in storage...")
            buckets.pop()
            store_order_delivery_state()
        else:
            logger.info(
                f"Warehouse has [{len(buckets)}] buckets in storage for pick up, adding more..."
            )
            analyze_storage_efficiency()
            add_buckets_to_storage()
        send_metrics(msg)
    except Exception as e:
        logger.info(f"Error processing MQTT message: {str(e)}")


capacity = None
buckets = []

count = 0

def counter():
    # Counter to count one up, and append to the count variable
 
    while True:
        count += 1
        logger.info(f"Counter is [{[count]}]")
        sleep(1)


def produce_bucket_notification():
    """Produce event to the warehouse topic that states a bucket is available in the warehouse for pickup."""
    logger.info("Notifying the production floor that a bucket is awaiting pick up...")


def add_buckets_to_storage():
    """Add received buckets into storage."""
    capacity = random.randint(1, 10)

    for bucket in range(capacity):
        logger.info(
            f"Warehouse received [{bucket + 1}] bucket(s) of reused Lego bricks... is now being stored for a robot arm to take."
        )
        buckets.append(bucket)

        sleep(0.5)


def analyze_storage_efficiency():
    """Track storage efficiency at random."""

    logger.info(
        "Storing efficiency measurement from the latest pool of finished buckets for future analysis..."
    )

    measurement = ["Efficient", "Inefficient", "Slow", "Reliable", "Fast", "Unreliable"]
    random_measurement = random.choice(measurement)

    # connection_cursor.execute("""INSERT INTO warehouse (efficiency) VALUES (%s)""", (random_measurement,))
    # postgres_connection.commit()


def store_order_delivery_state():
    """Store order delivery state at random."""

    logger.info("Storing order delivery state for future analysis...")

    state = [
        "Pending",
        "Processing",
        "Picked",
        "Packed",
        "Shipped",
        "Out of delivery",
        "Delivered",
    ]
    order_state = random.choice(state)

    # connection_cursor.execute("""INSERT INTO inventory (order_state) VALUES (%s)""", (order_state,))
    # postgres_connection.commit()


def send_metrics(message):
    global count
    
    """Send latency metrics to database"""
    json_data = json.loads(message.payload.decode("utf-8"))
    timestamp = json_data.get("timestamp")
    produced_timestamp_to_isoformat = datetime.datetime.fromtimestamp(
        timestamp
    ).isoformat()
    consumed_timestamp_to_isoformat = datetime.datetime.now().isoformat(
        timespec="seconds"
    )
    
    logger.info(f"Exact time difference [{count}] seconds")
    connection_cursor.execute("""INSERT INTO exactmqttlatency (time_diff) VALUES (%s)""", (count,))
    postgres_connection.commit()
    count = 0
    logger.info(f"Counter has been reset [{[count]}]")

    logger.info(
        f"Message was produced at [{produced_timestamp_to_isoformat}] and consumed at [{consumed_timestamp_to_isoformat}]"
    )
    connection_cursor.execute(
        """INSERT INTO mqttlatency (produced, consumed) VALUES (%s, %s)""",
        (
            produced_timestamp_to_isoformat,
            consumed_timestamp_to_isoformat,
        ),
    )
    postgres_connection.commit()


add_buckets_to_storage()
logger.info(f"Warehouse has [{len(buckets)}] bucket(s) in storage...")

# Produce first event that notifies a bucket is available.
produce_bucket_notification()

client = mqtt.Client()
client.on_message = on_message

client.connect(mqtt_broker, mqtt_port, 60)

client.subscribe("robotic_arms")

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

counter_thread = threading.Thread(target=counter)
counter_thread.start()
