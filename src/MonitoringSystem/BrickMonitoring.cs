using System;
using Confluent.Kafka;
using System.Threading;
using MongoDB.Driver;

public class BrickMonitoringSystem
{
    public static int redBricksCount = 0;
    public static int blueBricksCount = 0;
    public static int greenBricksCount = 0;
    public static IMongoCollection<BrickCountDocument> brickCountCollection;

    public static void Main()
    {
        string kafkaBrokerAddress = Environment.GetEnvironmentVariable("KAFKA_BROKER_ADDRESS");
        if (string.IsNullOrEmpty(kafkaBrokerAddress))
        {
            throw new InvalidOperationException("KAFKA_BROKER_ADDRESS environment variable not set.");
        }

        var mongoClient = var mongoClient = new MongoClient("mongodb://user:password@localhost:27017/brickmonitoringdb");
        var database = mongoClient.GetDatabase("brickmonitoringdb");
        brickCountCollection = database.GetCollection<BrickCountDocument>("brickcount");

        var config = new ConsumerConfig
        {
            GroupId = "brick-monitoring-group",
            BootstrapServers = kafkaBrokerAddress,
            AutoOffsetReset = AutoOffsetReset.Latest
        };

        using (var consumer = new ConsumerBuilder<Ignore, string>(config).Build())
        {
            consumer.Subscribe("brick-count-topic");

            while (true)
            {
                try
                {
                    var consumeResult = consumer.Consume();


                    string[] messageParts = consumeResult.Message.Value.Split(',');
                    if (messageParts.Length == 2)
                    {
                        int newCount = int.Parse(messageParts[0]);
                        string color = messageParts[1].Trim().ToLower();

                        UpdateBrickCount(color, newCount);

                        StoreBrickCountsInMongoDB(redBricksCount, blueBricksCount, greenBricksCount);
                    }
                }
                catch (ConsumeException e)
                {
                    Console.WriteLine($"Error consuming from Kafka: {e.Error.Reason}");
                }
            }
        }
    }

    public static void UpdateBrickCount(string color, int newCount)
    {
        if (color == "red")
        {
            redBricksCount += newCount;
        }
        else if (color == "blue")
        {
            blueBricksCount += newCount;
        }
        else if (color == "green")
        {
            greenBricksCount += newCount;
        }
    }

    public static void StoreBrickCountsInMongoDB(int redCount, int blueCount, int greenCount)
    {
        var document = new BrickCountDocument
        {
            RedCount = redCount,
            BlueCount = blueCount,
            GreenCount = greenCount
        };
        brickCountCollection.InsertOne(document);
    }
}

public class BrickCountDocument
{
    public int RedCount { get; set; }
    public int BlueCount { get; set; }
    public int GreenCount { get; set; }
}
