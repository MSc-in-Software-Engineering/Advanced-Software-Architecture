using Npgsql;
using Confluent.Kafka;
using System;
public class SchedulingSystem
{
    public void ScheduleTimeFromProduct(string kafkaBrokerServer, string topic)
    {
        var kafkaConf = new ConsumerConfig
        {
            BootstrapServers = kafkaBrokerServer,
            GroupId = "inventory-consumer-group-time",
            AutoOffsetReset = AutoOffsetReset.Earliest
        };

        using (var consumer = new ConsumerBuilder<Ignore, string>(kafkaConf).Build())
        {
            consumer.Subscribe(topic);
            Console.WriteLine($"Consuming values from : {topic}");
            try
            {
                while (true)
                {
                    var result = consumer.Consume();
                    if (result.Message.Value == "Processing")
                    {
                        Console.WriteLine($"Scheduling System: Production state: '{result.Message.Value}' at [{DateTime.Now}]");

                    }
                    else if (result.Message.Value == "Packed")
                    {
                        Console.WriteLine($"Scheduling System: Production state: '{result.Message.Value}' at [{DateTime.Now}]");
                    }
                }
            }
            catch (ConsumeException e)
            {
                Console.WriteLine($"Kafka topic ERROR: {e.Error}");
            }
        }
    }
}


class SchedulingProgram
{
    SchedulingSystem schedulingSystem = new SchedulingSystem();
    string kafkaTopic1 = "inventory";

    public void ProductionScheduleState(string kafkaBrokerServer)
    {
        if (!string.IsNullOrEmpty(kafkaBrokerServer))
        {
            schedulingSystem.ScheduleTimeFromProduct(kafkaBrokerServer, kafkaTopic1);
        }
        else
        {
            Console.WriteLine("kafka broker address not found");
        }
    }
}