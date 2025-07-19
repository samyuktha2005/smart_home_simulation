import time
import csv
from socket import *

serverName = 'nevedha'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)

# Create CSV file for logging client performance
with open('client_performance_data.csv', mode='w') as file:
    writer = csv.writer(file)
    writer.writerow(['timestamp', 'latency', 'endpoint'])

clientSocket.connect((serverName, serverPort))

command = input("Enter lighting command (on/off): ")
sentence = f"lighting {command}"

# Log timestamp and start time
start_time = time.time()
clientSocket.send(sentence.encode())

response = clientSocket.recv(1024).decode()
end_time = time.time()

# Log latency and endpoint
latency = end_time - start_time
with open('client_performance_data.csv', mode='a') as file:
    writer = csv.writer(file)
    writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), latency, "lighting"])

print("From server:", response)
clientSocket.close()
