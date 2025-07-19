import time
import csv
from socket import *

serverName = '192.168.100.4'
serverPort = 14000
clientSocket = socket(AF_INET, SOCK_STREAM)

# Create CSV file for logging client performance
csv_file = 'client_performance_data.csv'

# Initialize CSV file
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['timestamp', 'latency', 'endpoint', 'throughput'])

# Connect to the server
clientSocket.connect((serverName, serverPort))
command = input("Enter smart lock command (lock/unlock): ")
sentence = f"smartlock {command}"

# Log timestamp and start time
start_time = time.time()
clientSocket.send(sentence.encode())
bytes_sent = len(sentence.encode())  # Size of data sent

# Receive response from server
response = clientSocket.recv(1024).decode()
bytes_received = len(response.encode())  # Size of data received

end_time = time.time()

# Calculate latency
latency = end_time - start_time

# Calculate total data transferred and throughput
total_data_transferred = bytes_sent + bytes_received  # Total data in bytes
throughput = total_data_transferred / latency  # Bytes per second

# Log latency, endpoint, and throughput to CSV
with open(csv_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), latency, "smartlock", throughput])

# Output the server response and log details
print("From server:", response)
print(f"Logged to CSV: {time.strftime('%Y-%m-%d %H:%M:%S')}, {latency}, smartlock, {throughput:.2f} bytes/sec")

clientSocket.close()

