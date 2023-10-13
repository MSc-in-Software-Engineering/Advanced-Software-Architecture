import os
from confluent_kafka import Producer, Consumer, KafkaError
import logging

logger = logging.getLogger("warehouse_logger")

kafka_broker = os.environ.get("KAFKA_BROKER_ADDRESS")
kafka_group_id = "warehouse_group"
kafka_producer_topic = "warehouse"
kafka_consumer_topic = "mqtt_mediator"

class Bucket:
    def __init__(self, id):
        self.id = id

class Storage:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buckets = []
        self.kafka_producer = Producer({'bootstrap.servers': kafka_broker})
        self.kafka_consumer = Consumer({
            'bootstrap.servers': kafka_broker,
            'group.id': kafka_group_id,
            'auto.offset.reset': 'earliest'
        })
        self.kafka_consumer.subscribe([kafka_consumer_topic])

    def add_bucket(self, bucket):
        if len(self.buckets) < self.capacity:
            self.buckets.append(bucket)
            print(f'Bucket {bucket.id} added to storage.')
            self._send_to_kafka(f'Bucket {bucket.id} added to storage.')
        else:
            print('Storage is full. Cannot add more buckets.')

    def _send_to_kafka(self, message):
        self.kafka_producer.produce(kafka_producer_topic, key='bucket_event', value=message)
        self.kafka_producer.flush()

    def consume_from_kafka(self):
        while True:
            try:
                msg = self.kafka_consumer.poll(1.0)

                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(msg.error())
                        break

                print('Received message: {}'.format(msg.value()))
            except KafkaError as e:
                print(f"Kafka consumer error: {e}")

# Create a storage with a capacity of 5 buckets
storage = Storage(5)

# Add some buckets to the storage
for i in range(1, 6):
    bucket = Bucket(i)
    storage.add_bucket(bucket)

# Start consuming messages from Kafka
storage.consume_from_kafka()
