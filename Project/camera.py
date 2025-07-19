from socket import *
import time
import csv
from datetime import datetime

serverName = '192.168.100.4'
serverPortUDP = 14001
udpClientSocket = socket(AF_INET, SOCK_DGRAM)

# Record the start time
start_time = time.time()

message = "camera stream"
udpClientSocket.sendto(message.encode(), (serverName, serverPortUDP))

response, serverAddress = udpClientSocket.recvfrom(1024)
print("From server:", response.decode())

# Record the end time
end_time = time.time()

# Calculate latency
latency = end_time - start_time

# Log data to CSV
with open('client_performance_data.csv', mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([datetime.now(), latency, 'camera'])

udpClientSocket.close()

