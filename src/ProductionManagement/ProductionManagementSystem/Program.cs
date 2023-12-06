using Npgsql;
using Confluent.Kafka;

// Database connection to retrieve and insert values
public class Database
{
    private string databaseConnection = "Host=supply-chain-management-database;Port=5432;Username=postgres;Password=admin;Database=supplychainmanagement;";

    public void updateInventory(string amountOfBuckets)
    {
        Console.WriteLine("Update inventory");
        using (var dbConnection = new NpgsqlConnection(databaseConnection))
        {
            dbConnection.Open();
            Console.WriteLine("dbconnection open");
            string updateQuery = "INSERT INTO inventorymanagement (buckets_of_raw_materials) VALUES (@Buckets)";
            using (var sqlCMD = new NpgsqlCommand(updateQuery, dbConnection))
            {
                sqlCMD.Parameters.AddWithValue("Buckets", amountOfBuckets);
                Console.WriteLine("dbconnection insert");
                sqlCMD.ExecuteNonQuery();
            }
            dbConnection.Close();
        }
    }

    public void getInventoryData()
    {
        using (var dbConnection = new NpgsqlConnection(databaseConnection))
        {
            dbConnection.Open();
            string selectInventoryDataQuery = "SELECT * FROM inventorymanagement";

            using (var sqlCMD = new NpgsqlCommand(selectInventoryDataQuery, dbConnection))
            {
                using (var sqlReader = sqlCMD.ExecuteReader())
                {
                    while (sqlReader.Read())
                    {
                        Console.WriteLine($"ID: {sqlReader.GetInt32(0)}, Buckets: {sqlReader.GetInt32(1)}");
                    }
                }
            }
            dbConnection.Close();
        }
    }
}

// Kafka connector to consume values from specific topics
class KafkaConnector
{
    Database db = new Database();
    public void ConsumeFromKafkaTopic(string kafkaServers, string topic)
    {
        var kafkaConf = new ConsumerConfig
        {
            BootstrapServers = kafkaServers,
            GroupId = "inventory-consumer-group",
            AutoOffsetReset = AutoOffsetReset.Earliest
        };

        using (var consumer = new ConsumerBuilder<Ignore, string>(kafkaConf).Build())
        {
            consumer.Subscribe(topic);
            Console.WriteLine($"Consuming messages from topic: {topic}");
            try
            {
                while (true)
                {
                    var result = consumer.Consume();
                    if (topic == "capacity")
                    {
                        db.updateInventory(result.Message.Value);
                    }
                    else
                    {
                        Console.WriteLine($"Production of lego packets from {topic}: '{result.Message.Value}'");
                    }
                }
            }
            catch (ConsumeException e)
            {
                Console.WriteLine($"Error consume from kafka topic: {e.Error}");
            }
        }
    }

    public void ScheduleTimeFromProduct(string kafkaServers, string topic)
    {
        var kafkaConf = new ConsumerConfig
        {
            BootstrapServers = kafkaServers,
            GroupId = "inventory-consumer-group",
            AutoOffsetReset = AutoOffsetReset.Earliest
        };

        using (var consumer = new ConsumerBuilder<Ignore, string>(kafkaConf).Build())
        {
            consumer.Subscribe(topic);
            Console.WriteLine($"Consuming messages from topic: {topic}");
            try
            {
                while (true)
                {
                    var result = consumer.Consume();
                    if (result.Message.Value == "Processing")
                    {
                        Console.WriteLine($"[{DateTime.Now}] Scheduling System: Production state: '{result.Message.Value}'");

                    }
                    else if (result.Message.Value == "Packed")
                    {
                        Console.WriteLine($"[{DateTime.Now}] Scheduling System: Production state: '{result.Message.Value}'");
                    }
                }
            }
            catch (ConsumeException e)
            {
                Console.WriteLine($"Error consume from kafka topic: {e.Error}");
            }
        }
    }

}

// The scheduling system
class SchedulingSystem
{
    KafkaConnector kf = new KafkaConnector();
    string kafkaServers = Environment.GetEnvironmentVariable("KAFKA_BROKER_ADDRESS");
    string kafkaTopic1 = "inventory";

    public void ProductionScheduleState()
    {
        if (!string.IsNullOrEmpty(kafkaServers))
        {
            kf.ScheduleTimeFromProduct(kafkaServers, kafkaTopic1);
        }
        else
        {
            Console.WriteLine("kafka adress not found");
        }
    }
}

class Program
{
    static void Main(string[] args)
    {
        Database db = new Database();
        Console.WriteLine("PRODUCTION MANAGEMENT SYSTEM RUNNING");

        // Inventory management system
        KafkaConnector kf = new KafkaConnector();
        string kafkaServers = Environment.GetEnvironmentVariable("KAFKA_BROKER_ADDRESS");
        string kafkaTopic1 = "inventory";
        string kafkaTopic2 = "capacity";


        //Scheduling system
        SchedulingSystem ss = new SchedulingSystem();
        ss.ProductionScheduleState();

        if (!string.IsNullOrEmpty(kafkaServers))
        {
            kf.ConsumeFromKafkaTopic(kafkaServers, kafkaTopic1);
            kf.ConsumeFromKafkaTopic(kafkaServers, kafkaTopic2);

        }
        else
        {
            Console.WriteLine("kafka adress not found");
        }

        while (true)
        {
            db.getInventoryData();
        }
    }
}

