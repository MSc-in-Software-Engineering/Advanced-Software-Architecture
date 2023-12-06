using Npgsql;
using Confluent.Kafka;
using System;

public class Database
{
    private string databaseConnection = "Host=supply-chain-management-database;Port=5432;Username=postgres;Password=admin;Database=supplychainmanagement;";

    public void updateInventory(string amountOfBuckets)
    {
        Console.WriteLine("Update inventory");
        using (var dbConnection = new NpgsqlConnection(databaseConnection))
        {
            dbConnection.Open();
            Console.WriteLine("Database connection open");
            string updateQuery = "INSERT INTO inventorymanagement (buckets_of_raw_materials) VALUES (@Buckets)";
            using (var sqlCMD = new NpgsqlCommand(updateQuery, dbConnection))
            {
                sqlCMD.Parameters.AddWithValue("Buckets", amountOfBuckets);
                Console.WriteLine("Bucket updated in the database");
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

class KafkaConnector
{
    Database db = new Database();
    public void ConsumeFromKafkaTopics(string kafkaBrokerServer, List<string> kafkaTopics, string groupId)
    {
        var kafkaConf = new ConsumerConfig
        {
            BootstrapServers = kafkaBrokerServer,
            GroupId = groupId,
            AutoOffsetReset = AutoOffsetReset.Earliest
        };

        using (var consumer = new ConsumerBuilder<Ignore, string>(kafkaConf).Build())
        {
            consumer.Subscribe(kafkaTopics);
            try
            {
                while (true)
                {
                    var result = consumer.Consume();
                    if (kafkaTopics.Contains(result.Topic))
                    {
                        if (result.Topic == "capacity")
                        {
                            db.updateInventory(result.Message.Value);
                            Console.WriteLine($"Buckets of raw materials: '{result.Message.Value}'");

                        }
                        else
                        {
                            Console.WriteLine($"Production cycle of lego packets from the production line with the {result.Topic} topic: '{result.Message.Value}'");
                        }
                    }
                }
            }
            catch (ConsumeException e)
            {
                Console.WriteLine($"Kafka topics ERROR: {e.Error}");
            }
        }
    }

}

class IventorySystem
{
    public void StartInventorySystem(string kafkaBrokerServer)
    {
        Database db = new Database();
        Console.WriteLine("INVENTORY MANAGEMENT SYSTEM RUNNING");

        KafkaConnector kafkaconnection = new KafkaConnector();

        string kafkaTopic1 = "inventory";
        string kafkaTopic2 = "capacity";

        List<string> kafkaTopicsInventorySystem = new List<string> { kafkaTopic1, kafkaTopic2 };
        kafkaconnection.ConsumeFromKafkaTopics(kafkaBrokerServer, kafkaTopicsInventorySystem, "inventory-consumer-capacity");

        while (true)
        {
            db.getInventoryData();
        }
    }
}
