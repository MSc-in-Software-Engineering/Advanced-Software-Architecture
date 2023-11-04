import matplotlib.pyplot as plt
import datetime
import os
import psycopg2
import logging
from time import sleep

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("Metrics")

postgres_connection = psycopg2.connect(database="supplychainmanagement", user="postgres", password="admin", host="supply-chain-management-database", port="5432")
connection_cursor = postgres_connection.cursor()

connection_cursor.execute('SELECT produced FROM latency;')
produced_timestamps = [row[0].timestamp() for row in connection_cursor.fetchall()]

connection_cursor.execute('SELECT consumed FROM latency;')
consumed_timestamps = [row[0].timestamp() for row in connection_cursor.fetchall()]

produced_datetimes = [datetime.datetime.fromtimestamp(timestamp) for timestamp in produced_timestamps]
consumed_datetimes = [datetime.datetime.fromtimestamp(timestamp) for timestamp in consumed_timestamps]

time_differences = [(consumed_datetime - produced_datetime).total_seconds() for consumed_datetime, produced_datetime in zip(consumed_datetimes, produced_datetimes)]

def save_plot_to_folder(folder):
    """Save file to folder"""
    
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f'plot_{timestamp}.png'
    directory = f'plots/{folder}' 
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    plt.savefig(filepath)
    print(f"Plot saved as {filepath}")

def timeseries_line_chart():
    """Create timeseries line chart."""
    
    fig, ax = plt.subplots()
    
    ax.plot(produced_datetimes, time_differences, color='blue', marker='o')

    ax.set_title('Time Difference Between Produced and Consumed Events')
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Time Difference (Seconds)')

    plt.xticks(rotation=45)
    
    save_plot_to_folder("timeseries")
    
while(True):
    sleep(600)
    mean_time = sum(time_differences) / len(time_differences)
    logger.info(f'Mean is: {mean_time}')
    timeseries_line_chart()