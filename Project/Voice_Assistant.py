import time
import csv
import os
from socket import *

serverName = '192.168.100.4'
serverPort = 14001
clientSocket = socket(AF_INET, SOCK_DGRAM)

# Create CSV file for logging client performance
csv_file = 'client_performance_data.csv'

# Function to initialize CSV file
def initialize_csv(csv_file):
    if not os.path.exists(csv_file) or os.path.getsize(csv_file) == 0:
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['timestamp', 'latency', 'endpoint', 'throughput (bytes/sec)'])

initialize_csv(csv_file)

command = input("Enter voice assistant command: ")
sentence = f"voice_assistant {command}"

# Log timestamp and start time
start_time = time.time()

# Send the command to the server
clientSocket.sendto(sentence.encode(), (serverName, serverPort))
bytes_sent = len(sentence.encode())  # Size of data sent

# Receive response from the server
response, _ = clientSocket.recvfrom(2048)
end_time = time.time()
bytes_received = len(response)  # Size of data received (already in bytes)

# Calculate latency
latency = end_time - start_time

# Calculate total data transferred and throughput
total_data_transferred = bytes_sent + bytes_received  # Total data in bytes
throughput = total_data_transferred / latency  # Bytes per second

# Log latency, endpoint, and throughput
with open(csv_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), latency, "voice_assistant", throughput])

# Print the server response and log details
print("From server:", response.decode())
print(f"Logged to CSV: {time.strftime('%Y-%m-%d %H:%M:%S')}, {latency}, voice_assistant, {throughput:.2f} bytes/sec")

clientSocket.close()

