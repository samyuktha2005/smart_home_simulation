import time
import csv
from socket import *

serverName = '192.168.100.4'
serverPort = 14000
clientSocket = socket(AF_INET, SOCK_STREAM)

# Create CSV file for logging client performance
csv_file = 'client_performance_data.csv'

# Initialize the CSV file with headers
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['timestamp', 'latency', 'endpoint', 'throughput'])

# Connect to the server
clientSocket.connect((serverName, serverPort))
command = input("Enter lighting command (on/off): ")
sentence = f"lighting {command}"

# Log timestamp and start time
start_time = time.time()
clientSocket.send(sentence.encode())

response = clientSocket.recv(1024).decode()
end_time = time.time()

# Calculate latency
latency = end_time - start_time

# Calculate throughput
bytes_sent = len(sentence.encode())
bytes_received = len(response.encode())
total_data_transferred = bytes_sent + bytes_received  # Total data in bytes
throughput = total_data_transferred / latency  # Bytes per second

# Log latency, throughput, and endpoint
with open(csv_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), latency, "lighting", throughput])

print("From server:", response)
print(f"Logged to CSV: {time.strftime('%Y-%m-%d %H:%M:%S')}, {latency}, lighting, {throughput:.2f} bytes/sec")

clientSocket.close()

