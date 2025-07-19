import time
import csv
import os
from socket import *

serverName = '192.168.100.4'
serverPort = 14000
clientSocket = socket(AF_INET, SOCK_STREAM)

# Create CSV file for logging client performance
csv_file = 'client_performance_data.csv'


with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['timestamp', 'latency', 'endpoint','throughput'])

    # Connect to the server
    clientSocket.connect((serverName, serverPort))
    command = input("Enter cooking appliance command (start/stop): ")
    sentence =f"cooking {command}"

    # Log timestamp and start time
    start_time = time.time()
    clientSocket.send(sentence.encode())
    bytes_sent = len(sentence.encode())
    
    response = clientSocket.recv(1024).decode()
    end_time = time.time()
    bytes_received = len(response.encode())
    
    # Calculate latency
    latency = end_time - start_time
    
    # Calculate total data transferred and throughput

    total_data_transferred = bytes_sent + bytes_received  # Total data in bytes
    throughput = total_data_transferred / latency  # Bytes per second  
    
    # Log latency and endpoint
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), latency, "cooking", throughput])
    
    print("From server:", response)
    print(f"Logged to CSV: {time.strftime('%Y-%m-%d %H:%M:%S')}, {latency}, cooking, {throughput:.2f} bytes/sec")

    clientSocket.close()

