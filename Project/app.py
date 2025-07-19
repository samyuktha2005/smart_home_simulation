from flask import Flask, request, jsonify, render_template
import socket
import time
import csv
import os
import pandas as pd
import matplotlib

# Set the backend for matplotlib to Agg to avoid Tkinter-related errors
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)

# Server IP and port numbers for TCP and UDP
serverName = '192.168.100.4'
tcpPort = 14000
udpPort = 14001
csv_file = 'client_performance_data.csv'

# Initialize the CSV file with headers if it doesn't exist
if not os.path.exists(csv_file) or os.path.getsize(csv_file) == 0:
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'latency', 'protocol', 'endpoint'])

def send_tcp_command_to_server(command, endpoint):
    start_time = time.time()
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
        clientSocket.connect((serverName, tcpPort))
        clientSocket.send(command.encode())
        response = clientSocket.recv(1024).decode()
        
    end_time = time.time()
    
    # Calculate latency
    latency = end_time - start_time
    
    # Log latency and endpoint to the CSV file
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), latency, 'TCP', endpoint])
    
    return response

def send_udp_command_to_server(command, endpoint):
    start_time = time.time()
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as clientSocket:
        clientSocket.sendto(command.encode(), (serverName, udpPort))
        response, _ = clientSocket.recvfrom(1024)
        
    end_time = time.time()
    
    # Calculate latency
    latency = end_time - start_time
    
    # Log latency and endpoint to the CSV file
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), latency, 'UDP', endpoint])
    
    return response.decode()

def create_graph():
    # Read client performance data with timestamps
    client_data = pd.read_csv('client_performance_data.csv', parse_dates=['timestamp'])

    # Convert latency to milliseconds
    client_data['latency_ms'] = client_data['latency'] * 1000

    ### Client-Side Latency per Protocol and Endpoint
    client_latency = client_data.groupby(['protocol', 'endpoint'])['latency_ms'].mean().reset_index()

    plt.figure(figsize=(10, 5))
    client_latency.pivot("endpoint", "protocol", "latency_ms").plot(kind='bar')
    plt.title('Average Client-Side Latency per Protocol and Endpoint')
    plt.xlabel('Endpoint')
    plt.ylabel('Latency (ms)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/client_latency_per_protocol_endpoint.png')

    ### Client-Side Latency Distribution
    plt.figure(figsize=(10, 5))
    plt.hist(client_data['latency_ms'], bins=20, color='skyblue', edgecolor='black')
    plt.title('Client-Side Latency Distribution')
    plt.xlabel('Latency (ms)')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig('static/client_latency_distribution.png')

    ### Throughput Analysis (Client-Side)
    client_data.set_index('timestamp', inplace=True)
    client_throughput = client_data['endpoint'].resample('1T').count()

    plt.figure(figsize=(10, 5))
    client_throughput.plot(kind='line', marker='o')
    plt.title('Client-Side Throughput Over Time')
    plt.xlabel('Time')
    plt.ylabel('Number of Requests per Minute')
    plt.tight_layout()
    plt.savefig('static/client_throughput.png')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analysis')
def analysis():
    create_graph()  # Generate the graph
    return render_template('analysis.html')

# Adding the cooking appliance endpoint
@app.route('/cooking', methods=['POST'])
def control_cooking():
    command = request.form.get('command')
    if command:
        response = send_tcp_command_to_server(f"cooking {command}", "cooking")
        return jsonify({'response': response})
    return jsonify({'response': 'No cooking command provided'})

# Adding the smart lock endpoint
@app.route('/smartlock', methods=['POST'])
def control_smart_lock():
    command = request.form.get('command')
    if command:
        response = send_tcp_command_to_server(f"smartlock {command}", "smartlock")
        return jsonify({'response': response})
    return jsonify({'response': 'No lock command provided'})

# Adding the voice assistant endpoint (UDP-based)
@app.route('/voice_assistant', methods=['POST'])
def control_voice_assistant():
    command = request.form.get('command')
    if command:
        response = send_udp_command_to_server(f"voice_assistant {command}", "voice_assistant")
        return jsonify({'response': response})
    return jsonify({'response': 'No voice command provided'})

@app.route('/light', methods=['POST'])
def control_light():
    command = request.form.get('command')
    if command:
        response = send_tcp_command_to_server(f"lighting {command}", "lighting")
        return jsonify({'response': response})
    return jsonify({'response': 'No command provided'})

@app.route('/thermostat', methods=['POST'])
def set_thermostat():
    temperature = request.form.get('temperature')
    if temperature:
        response = send_tcp_command_to_server(f"thermostat {temperature}", "thermostat")
        return jsonify({'response': response})
    return jsonify({'response': 'No temperature provided'})

@app.route('/security', methods=['POST'])
def control_security():
    command = request.form.get('command')
    if command:
        response = send_tcp_command_to_server(f"security {command}", "security")
        return jsonify({'response': response})
    return jsonify({'response': 'No security command provided'})

@app.route('/camera', methods=['POST'])
def send_camera_data():
    response = send_udp_command_to_server("camera data", "camera")
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
