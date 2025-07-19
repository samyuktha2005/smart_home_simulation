from socket import *
import time
import csv
from datetime import datetime

serverName = 'localhost'  # Use appropriate hostname or IP address
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# Input temperature
temperature = input("Set thermostat temperature (in degrees): ")

# Record the start time
start_time = time.time()

# Send thermostat command
sentence = f"thermostat {temperature}"
clientSocket.send(sentence.encode())

response = clientSocket.recv(1024).decode()
print("From server:", response)

# Record the end time
end_time = time.time()

# Calculate latency
latency = end_time - start_time

# Log data to CSV
with open('client_performance_data.csv', mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([datetime.now(), latency, 'thermostat'])

clientSocket.close()
