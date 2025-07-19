import time
import csv
from socket import *
import os

# Server details
serverName = '192.168.100.4'
serverPort = 14000
clientSocket = socket(AF_INET, SOCK_STREAM)

# Create CSV file for logging client performance
csv_file_path = os.path.join(os.getcwd(), 'client_performance_data.csv')
try:
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'latency', 'endpoint', 'throughput'])  # Added throughput column
except Exception as e:
    print(f"Error creating CSV file: {e}")

try:
    clientSocket.connect((serverName, serverPort))

    # Take lighting command from user
    command = input("Enter temperature")
    sentence = f"thermostat {command}"

    # Log timestamp and start time
    start_time = time.time()
    clientSocket.send(sentence.encode())

    # Receive and decode response
    response = clientSocket.recv(1024).decode()

    # Log end time and calculate latency
    end_time = time.time()
    latency = end_time - start_time

    # Calculate throughput
    bytes_sent = len(sentence.encode())
    bytes_received = len(response.encode())
    total_data_transferred = bytes_sent + bytes_received
    throughput = total_data_transferred / latency if latency > 0 else 0  # Bytes per second

    # Append data to CSV
    try:
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), latency, "thermostat", throughput])  # Added throughput
            file.flush()  # Ensure data is written to the file immediately
    except Exception as e:
        print(f"Error writing to CSV file: {e}")

    print("From server:", response)
    
finally:
    # Close the socket
    clientSocket.close()

