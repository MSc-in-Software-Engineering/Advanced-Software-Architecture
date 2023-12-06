class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("SCHEDULING SYSTEM RUNNING");

        string kafkaServers = Environment.GetEnvironmentVariable("KAFKA_BROKER_ADDRESS");

        SchedulingProgram ss = new SchedulingProgram();
        ss.ProductionScheduleState(kafkaServers);
    }
}