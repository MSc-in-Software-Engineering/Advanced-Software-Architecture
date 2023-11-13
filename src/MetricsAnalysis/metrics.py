import matplotlib.pyplot as plt
import datetime
import os
import psycopg2
import logging
from time import sleep

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("Metrics")

postgres_connection = psycopg2.connect(
    database="supplychainmanagement",
    user="postgres",
    password="admin",
    host="supply-chain-management-database",
    port="5432",
)
connection_cursor = postgres_connection.cursor()


def save_plot_to_folder(folder, number):
    """Save file to folder"""

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"plot_{timestamp}_{number}.png"
    directory = f"plots/{folder}"
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    plt.savefig(filepath)
    print(f"Plot saved as {filepath}")


def line_chart(table, number, title):
    try:
        """Create timeseries line chart."""
        connection_cursor.execute(f"SELECT produced FROM {table};")
        produced_timestamps = [row[0].timestamp() for row in connection_cursor.fetchall()]

        connection_cursor.execute(f"SELECT consumed FROM {table};")
        consumed_timestamps = [row[0].timestamp() for row in connection_cursor.fetchall()]

        produced_datetimes = [
            datetime.datetime.fromtimestamp(timestamp) for timestamp in produced_timestamps
        ]
        consumed_datetimes = [
            datetime.datetime.fromtimestamp(timestamp) for timestamp in consumed_timestamps
        ]

        time_differences = [
            (consumed_datetime - produced_datetime).total_seconds()
            for consumed_datetime, produced_datetime in zip(
                consumed_datetimes, produced_datetimes
            )
        ]

        fig, ax = plt.subplots()

        ax.plot(produced_datetimes, time_differences, color="blue", marker="o")

        ax.set_title("Time Difference Between Produced and Consumed Events")
        ax.set_xlabel("Timestamp")
        ax.set_ylabel("Time Difference (Seconds)")

        plt.xticks(rotation=45)

        save_plot_to_folder(f"linechart/{title}", number)

        mean_time = sum(time_differences) / len(time_differences)
        logger.info(f"{title} Mean is: {mean_time}")
    except ZeroDivisionError:
        pass
    
    
def box_plot(table, number, title):
    """Create timeseries boxplot."""
    connection_cursor.execute(f"SELECT produced FROM {table};")
    produced_timestamps = [row[0].timestamp() for row in connection_cursor.fetchall()]

    connection_cursor.execute(f"SELECT consumed FROM {table};")
    consumed_timestamps = [row[0].timestamp() for row in connection_cursor.fetchall()]

    produced_datetimes = [
        datetime.datetime.fromtimestamp(timestamp) for timestamp in produced_timestamps
    ]
    consumed_datetimes = [
        datetime.datetime.fromtimestamp(timestamp) for timestamp in consumed_timestamps
    ]

    time_differences = [
        (consumed_datetime - produced_datetime).total_seconds()
        for consumed_datetime, produced_datetime in zip(
            consumed_datetimes, produced_datetimes
        )
    ]

    fig, ax = plt.subplots()

    ax.boxplot(time_differences)

    ax.set_title("Time Difference Between Produced and Consumed Events")
    ax.set_xlabel("Time Difference (Seconds)")

    save_plot_to_folder(f"boxplot/{title}", number)


while True:
    sleep(600)
    line_chart("latency", 0, "Kafka")
    line_chart("mqttlatency", 1, "MQTT")
    box_plot("latency", 0, "Kafka")
    box_plot("mqttlatency", 1, "MQTT")
