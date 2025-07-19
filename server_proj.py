import time
import csv
from socket import *
import select

# Function to handle thermostat commands
def handle_thermostat(data):
    try:
        temperature = int(data.split()[1])
    except (IndexError, ValueError):
        return "Invalid data format"

    if 10 < temperature < 30:
        response = f"Thermostat set to {temperature} degrees."
    else:
        response = f"Temperature {temperature} degrees is out of range."
    return response

# Function to handle lighting commands
def handle_lighting(data):
    command = data.split()[1].lower()
    if command == "on":
        response = "Lights turned ON."
    elif command == "off":
        response = "Lights turned OFF."
    else:
        response = "Invalid lighting command."
    return response

# Function to handle camera commands
def handle_camera(data):
    return "Camera data received."

# Function to handle cooking commands
def handle_cooking(data):
    try:
        command = data.split()[1].lower()
        if command == "start":
            response = "Cooking started."
        elif command == "stop":
            response = "Cooking stopped."
        else:
            response = "Invalid cooking command."
    except IndexError:
        response = "Invalid cooking command format."
    return response

# Function to handle voice assistant commands
def handle_voice_assistant(data):
    command = data.split()[1].lower()
    if command == "activate":
        response = "Voice assistant activated."
    elif command == "deactivate":
        response = "Voice assistant deactivated."
    else:
        response = "Invalid voice assistant command."
    return response

# Function to handle smart lock commands
def handle_smart_lock(data):
    command = data.split()[1].lower()
    if command == "lock":
        response = "Smart lock engaged."
    elif command == "unlock":
        response = "Smart lock disengaged."
    else:
        response = "Invalid smart lock command."
    return response
# Initialize CSV file for logging server performance
def initialize_csv(file_name):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'latency', 'endpoint'])

# Function to log server performance data
def log_performance(file_name, latency, endpoint):
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), latency, endpoint])

csv_file = 'server_performance_data.csv'
initialize_csv(csv_file)

# TCP Server setup
serverPortTCP = 14000
tcpSocket = socket(AF_INET, SOCK_STREAM)
tcpSocket.bind(('', serverPortTCP))
tcpSocket.listen(5)
tcpSocket.setblocking(False)
print("The TCP server is ready to receive on port 14000")

# UDP Server setup (assigning different port)
serverPortUDP = 14001
udpSocket = socket(AF_INET, SOCK_DGRAM)
udpSocket.bind(('', serverPortUDP))
udpSocket.setblocking(False)
print("The UDP server is ready to receive on port 14001")

# Server loop for handling both TCP and UDP requests concurrently
sockets_list = [tcpSocket, udpSocket]

while True:
    readable, _, _ = select.select(sockets_list, [], [])

    for sock in readable:
        # Handle TCP requests
        if sock == tcpSocket:
            try:
                connectionSocket, addr = tcpSocket.accept()
                print(f"TCP client connected from {addr}")

                # Log start time for performance tracking
                start_time = time.time()

                # Receive and process the TCP request
                sentence = connectionSocket.recv(1024).decode()
                function_type = sentence.split()[0].lower()

                if function_type == "thermostat":
                    response = handle_thermostat(sentence)
                elif function_type == "lighting":
                    response = handle_lighting(sentence)
                elif function_type == "cooking":
                    response = handle_cooking(sentence)
                elif function_type == "smartlock":
                    response = handle_smart_lock(sentence)
                else:
                    response = "Unknown function requested."

                # Send response back to the client
                connectionSocket.send(response.encode())
                connectionSocket.close()

                # Log latency and endpoint
                end_time = time.time()
                latency = end_time - start_time
                log_performance(csv_file, latency, function_type)

            except Exception as e:
                print(f"Error handling TCP request: {e}")

        # Handle UDP requests
        elif sock == udpSocket:
            try:
                data, addr = udpSocket.recvfrom(1024)
                print(f"UDP client connected from {addr}")

                # Log start time for performance tracking
                start_time = time.time()
                sentence = data.decode()
                function_type = sentence.split()[0].lower()

                # Process the UDP request based on the function type
                if function_type == "camera":
                    response = handle_camera(sentence)
                    endpoint = "camera"
                elif function_type == "voice_assistant":
                    response = handle_voice_assistant(sentence)
                    endpoint = "voice_assistant"
                else:
                    response = "Unknown function requested."
                    endpoint = "unknown"

                # Send response back to the UDP client
                udpSocket.sendto(response.encode(), addr)

                # Log latency and endpoint
                end_time = time.time()
                latency = end_time - start_time
                log_performance(csv_file, latency, endpoint)

            except Exception as e:
                print(f"Error handling UDP request: {e}")
