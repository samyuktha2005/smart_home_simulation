from socket import *

def handle_thermostat(data):
    try:
        temperature = int(data.split()[1])
    except:
        response = f"Invalid data format"
        return response

    if 10 < temperature < 30:
        response = f"Thermostat set to {temperature} degrees."
    else:
        response = f"Temperature {temperature} degrees is out of range."
    return response

def handle_lighting(data):
    command = data.split()[1].lower()
    if command == "on":
        response = "Lights turned ON."
    elif command == "off":
        response = "Lights turned OFF."
    else:
        response = "Invalid lighting command."
    return response

def handle_camera(data):
    response = "Camera data received."
    return response

# Setting up TCP server
serverPort = 14000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print("The TCP server is ready to receive commands")

while True:
    connectionSocket, addr = serverSocket.accept()
    print(f"Connected to {addr}")

    sentence = connectionSocket.recv(1024).decode()
    function_type = sentence.split()[0].lower()

    if function_type == "thermostat":
        response = handle_thermostat(sentence)
    elif function_type == "lighting":
        response = handle_lighting(sentence)
    elif function_type == "camera":
        response = handle_camera(sentence)
    else:
        response = "Unknown function requested."

    connectionSocket.send(response.encode())
    connectionSocket.close()
