"""Storing finished goods, Manage inventory levels, Stores safely and efficiently """

import logging
import os
import random
import psycopg2
from time import sleep
from confluent_kafka import Producer, Consumer

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("Warehouse")

postgres_connection = psycopg2.connect(database="supplychainmanagement", user="postgres", password="admin", host="supply-chain-management-database", port="5432")
connection_cursor = postgres_connection.cursor()

kafka_broker = os.environ.get("KAFKA_BROKER_ADDRESS")
kafka_group_id = "warehouse_group"
kafka_producer_topic = ("warehouse", "efficiency")
kafka_consumer_topic = "production-cycle"
kafka_producer = Producer({"bootstrap.servers": kafka_broker})
kafka_consumer = Consumer(
    {
        "bootstrap.servers": kafka_broker,
        "group.id": kafka_group_id,
        "auto.offset.reset": "earliest",
    }
)
kafka_consumer.subscribe([kafka_consumer_topic])

capacity = random.randint(1, 10)
buckets = []


def produce_bucket_notification():
    """Produce event to the warehouse topic that states a bucket is available in the warehouse for pickup."""
    logger.info("Notifying the production floor that a bucket is awaiting pick up...")

    kafka_producer.produce(
        kafka_producer_topic[0],
        key="bucket_event",
        value="A bucket is in storage at the warehouse and is awaiting pick up...",
    )
    kafka_producer.flush()


def consume_production_cycles():
    """Consume events from the production-cycle topic that monitors if a full production cycle has been finished."""

    while True:
        message = kafka_consumer.poll(timeout=1.0)
        if message is None:
            continue
        elif message.error():
            logger.warning(
                f"The topic [{kafka_consumer_topic}] is not available for utilization..."
            )
            logger.info(
                f"Trying to consume from the topic [{kafka_consumer_topic}] in 5 minutes..."
            )
            sleep(300)
        else:
            if len(buckets) != 0:
                produce_bucket_notification()
                logger.info(f"Warehouse has [{len(buckets)}] bucket(s) in storage...")
                buckets.pop()
            else:
                logger.info(
                    f"Warehouse has [{len(buckets)}] buckets in storage for pick up, adding more..."
                )
                analyze_storage_efficiency()
                add_buckets_to_storage()
                

def add_buckets_to_storage():
    """Add received buckets into storage."""
    
    for bucket in range(capacity):
        logger.info(
            f"Warehouse received [{bucket + 1}] bucket(s) of reused Lego bricks... is now being stored for a robot arm to take."
        )
        buckets.append(bucket)

        sleep(0.5)
        
def analyze_storage_efficiency():
    """Track storage efficiency at random."""
    
    logger.info("Storing efficiency measurement from the latest pool of finished buckets for future analysis...")
    
    measurement = ["Efficient", "Inefficient", "Slow", "Reliable", "Fast", "Unreliable"]
    random_measurement = random.choice(measurement)
    
    kafka_producer.produce(
        kafka_producer_topic[1],
        key="efficiency_event",
        value=random_measurement,
    )
    kafka_producer.flush()
    
    connection_cursor.execute("""INSERT INTO warehouse (efficiency) VALUES (%s)""", (random_measurement,))
    postgres_connection.commit()

add_buckets_to_storage()

logger.info(f"Warehouse has [{len(buckets)}] bucket(s) in storage...")

# Produce first event that notifies a bucket is available.
produce_bucket_notification()

analyze_storage_efficiency()

# Listening to production cycle events until warehouse is empty of buckets.
consume_production_cycles()
