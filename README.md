# 🏡 smart_home_simulation
Here is your **updated, GitHub-ready `README.md`** for your **“Integrating Smart Home System using UDP and TCP Protocols”** project, explicitly mentioning:

✅ Done between **two Ubuntu systems of different versions**.
✅ One system runs the **device hub + devices (uploaded zip)**, the other runs **`server.py`** for handling device communication and control.

# Integrating Smart Home System Using UDP and TCP Protocols

This project integrates a **smart home system** using **UDP and TCP protocols (not including IoT cloud)**, focusing on **network communication and protocol management** between devices within a local environment.

✅ **Tested between two Ubuntu systems of different versions:**
- **Ubuntu System 1**: Runs device hub, devices, and Flask dashboard (uploaded ZIP).
- **Ubuntu System 2**: Runs `server.py` to handle communication and device control using UDP/TCP protocols.

---

## 🚀 Features

- **Local Device Simulation**:
  - Camera, lights, thermostat, smart lock, washing machine, cooking appliances simulated as Python scripts communicating with the hub using TCP/UDP.
- **Central Hub** (`hub.py`):
  - Registers devices dynamically.
  - Sends control commands and receives device statuses.
- **Server Coordination** (`server.py` on the second Ubuntu system):
  - Handles device registration, control requests, and reliable UDP/TCP communication.
- **Performance Logging**:
  - Latency and throughput data captured in `client_performance_data.csv` and `server_performance_data.csv`.
- **Data Analysis & Visualization**:
  - Generates latency distribution and throughput graphs.
  - Endpoint-wise performance tracking.
- **Web Dashboard (Flask)**:
  - Control devices through a simple web interface.
  - Visualize real-time device statuses and performance.

---

## 🗂️ Project Structure

- `app.py`: Flask server for the web dashboard.
- `hub.py`: Main device hub manager.
- `network_control.py`: UDP/TCP socket handling.
- `camera.py`, `light.py`, `thermostat.py`, etc.: Device scripts.
- `Voice_Assistant.py`: Voice control for devices.
- `*_analysis.py`: Data analysis and visualization scripts.
- `server.py`: **(On second Ubuntu system)** Manages device communication over TCP/UDP.
- `templates/`, `static/`: Web dashboard HTML and images.
- `client_performance_data.csv`, `server_performance_data.csv`: Logs of latency and throughput data.
- `styles.css`: Dashboard styling.

---

## ⚙️ How to Run

### 1️⃣ Install Requirements

On both Ubuntu systems:
```bash
pip install flask matplotlib pandas numpy
````

---

### 2️⃣ On Ubuntu System 1 (Hub + Devices + Dashboard)

#### ✅ Start the Hub:

```bash
python hub.py
```

#### ✅ Start Devices:

In separate terminals:

```bash
python camera.py
python light.py
python thermostat.py
python smartlock.py
python washing_machine.py
python cooking.py
```

#### ✅ Start the Flask Dashboard:

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser to control and view devices.

---

### 3️⃣ On Ubuntu System 2 (server.py)

Run:

```bash
python server.py
```

This will handle:

* Device registration from Ubuntu System 1 over the network.
* Command/control management over UDP and TCP.
* Logging of performance metrics.

---

### 4️⃣ (Optional) Run Data Analysis

To visualize latency and throughput graphs:

```bash
python camera_analysis.py
python light_analysis.py
python thermostat_analysis.py
python hub_analysis.py
```

Graphs will be saved in the `static/` folder and viewable via the dashboard.

---

## 📈 What You Get

✅ Fully **local smart home system** without cloud dependencies.
✅ Understand **TCP vs UDP communication** practically.
✅ Web dashboard for monitoring and controlling devices.
✅ Performance analysis to study the efficiency of your network.

---

## 📌 Notes

* Designed for **networks and protocol understanding**.
* Focuses on device integration using **UDP (fast status updates) and TCP (reliable commands)**.
* Can be extended with encryption and device authentication for security learning.

---

## 📜 License

[MIT License](LICENSE)

---

## 🤝 Contributions

Contributions to improve device simulation, add security layers, or optimize the network stack are welcome.


