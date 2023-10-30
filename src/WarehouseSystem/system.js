const { Kafka } = require("kafkajs");

const kafka = new Kafka({
  clientId: "warehouse-system",
  brokers: [`${process.env.KAFKA_BROKER_ADDRESS}:9092`],
});

const consumer = kafka.consumer({ groupId: "warehouse-group" });

const run = async () => {
  await consumer.connect();
  await consumer.subscribe({ topics: ["warehouse", "efficiency"] });

  await consumer.run({
    eachMessage: async ({ message }) => {
      console.log({
        timestamp: message.timestamp,
        value: message.value.toString(),
      });
    },
  });
};

run().catch(console.error);
