using Npgsql;
using Confluent.Kafka;
using System;

class Program
{
    static void Main(string[] args)
    {
        string kafkaBrokerServer = Environment.GetEnvironmentVariable("KAFKA_BROKER_ADDRESS");
        IventorySystem invs = new IventorySystem();
        invs.StartInventorySystem(kafkaBrokerServer);
    }
}

