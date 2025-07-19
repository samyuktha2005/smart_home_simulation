import time
import csv
from socket import *

def handle_thermostat(data):
    temperature = int(data.split()[1])
    if 10 < temperature < 30:
        response = f"Thermostat set to {temperature} degrees."
    else:
        response = f"Temperature {temperature} degrees is out of range."
    return response

def handle_lighting(data):
    command = data.split()[1]
    if command.lower() == "on":
        response = "Lights turned ON."
    elif command.lower() == "off":
        response = "Lights turned OFF."
    else:
        response = "Invalid lighting command."
    return response

def handle_camera(data):
    response = "Camera data received."
    return response

# Create CSV file for logging server performance
with open('server_performance_data.csv', mode='w') as file:
    writer = csv.writer(file)
    writer.writerow(['timestamp', 'latency', 'endpoint'])

serverPortTCP = 12000
tcpSocket = socket(AF_INET, SOCK_STREAM)
tcpSocket.bind(('', serverPortTCP))
tcpSocket.listen(1)
print("The TCP server is ready to receive")

serverPortUDP = 13000
udpSocket = socket(AF_INET, SOCK_DGRAM)
udpSocket.bind(('', serverPortUDP))
print("The UDP server is ready to receive")

while True:
    tcpSocket.settimeout(1)
    udpSocket.settimeout(1)

    try:
        connectionSocket, addr = tcpSocket.accept()
        print(f"TCP client connected from {addr}")
        
        # Log timestamp
        start_time = time.time()
        
        sentence = connectionSocket.recv(1024).decode()
        function_type = sentence.split()[0].lower()
        
        if function_type == "thermostat":
            response = handle_thermostat(sentence)
        elif function_type == "lighting":
            response = handle_lighting(sentence)
        else:
            response = "Unknown function requested."

        connectionSocket.send(response.encode())
        connectionSocket.close()
        
        # Log latency and endpoint
        end_time = time.time()
        latency = end_time - start_time
        with open('server_performance_data.csv', mode='a') as file:
            writer = csv.writer(file)
            writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), latency, function_type])

    except timeout:
        pass

    try:
        data, addr = udpSocket.recvfrom(1024)
        print(f"UDP client (camera) connected from {addr}")
        
        start_time = time.time()
        
        response = handle_camera(data.decode())
        udpSocket.sendto(response.encode(), addr)
        
        end_time = time.time()
        latency = end_time - start_time
        with open('server_performance_data.csv', mode='a') as file:
            writer = csv.writer(file)
            writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), latency, "camera"])

    except timeout:
        pass
