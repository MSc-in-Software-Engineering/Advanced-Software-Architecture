import logging
import os
import random
from time import sleep
from confluent_kafka import Producer, Consumer

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("Warehouse")


kafka_broker = os.environ.get("KAFKA_BROKER_ADDRESS")
kafka_group_id = "warehouse_group"
kafka_producer_topic = "warehouse"
kafka_consumer_topic = "mqtt_mediator"
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
        kafka_producer_topic,
        key="bucket_event",
        value="A bucket is in storage at the warehouse and is awaiting pick up...",
    )
    kafka_producer.flush()


def consume_production_cycles():
    """Consume events from the mqtt-mediator topic that monitors if a full production cycle has been finished."""

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
                    f"Warehouse has [{len(buckets)}] buckets in storage for pick up..."
                )
                kafka_consumer.close()


for bucket in range(capacity):
    logger.info(
        f"Warehouse received [{bucket + 1}] bucket(s) of reused Lego bricks... is now being stored for a robot arm to take."
    )
    buckets.append(bucket)

    sleep(0.5)

logger.info(f"Warehouse has [{len(buckets)}] bucket(s) in storage...")

# Produce first event that notifies a bucket is available.
produce_bucket_notification()

# Listening to production cycle events until warehouse is empty of buckets.
consume_production_cycles()
