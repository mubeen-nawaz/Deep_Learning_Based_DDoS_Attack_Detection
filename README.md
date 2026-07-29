# Deep Learning Based DDoS Attack Detection

A network intrusion detection system that uses an LSTM neural network to classify live network traffic as **normal** or **DDoS** in real time. The project includes the model training notebooks, a Flask + Socket.IO dashboard for live monitoring, a packet sniffer that feeds live traffic into the model, and simple scripts to simulate a victim server and a SYN-flood attack for local testing.

> ⚠️ **For educational and research use only.** The attack simulation script (`attack.py`) generates SYN-flood traffic. Only run it against systems you own or have explicit permission to test, and only on isolated/local networks.

## How it works

1. **Model training** (notebooks) — Flow-level network traffic features (e.g. from the CIC-DDoS2019 `Portmap.csv` dataset) are used to train and compare an SVM, a CNN, and an LSTM classifier. The LSTM model is exported as `lstm_ddos_model.h5` along with its fitted `scaler.pkl`.
2. **Live capture** (`sniffer.py`) — Uses `pyshark` to sniff packets from a network interface, extracts a feature vector per packet, and streams it to the detection server over Socket.IO.
3. **Detection server** (`app.py`) — A Flask + Flask-SocketIO server loads the trained LSTM model and scaler, scales incoming features, and predicts the probability of an attack. It smooths predictions over the last 10 packets to reduce false alarms and pushes `traffic_update` / `ddos_alert` events to connected clients.
4. **Dashboard** (`templates/index.html`) — A real-time web UI ("Sentinel IDS") that visualizes traffic load and displays live threat alerts using Chart.js and Socket.IO.
5. **Test harness** (`victime_site.py`, `attack.py`) — A mock "victim" web server and a SYN-flood script you can use to generate attack traffic locally and validate that the pipeline detects it.

## Project structure

```
.
├── app.py                                   # Flask + Socket.IO detection server
├── sniffer.py                                # Live packet capture -> feature extraction -> server
├── attack.py                                 # SYN-flood traffic generator (for local testing)
├── victime_site.py                           # Mock victim web server (Flask, port 8080)
├── templates/
│   └── index.html                            # Real-time monitoring dashboard
├── lstm_ddos_model.h5                        # Trained LSTM model
├── scaler.pkl                                # Fitted StandardScaler used at inference time
├── DDoS_LSTM.ipynb                           # LSTM training notebook
├── DDoS_Detection_LSTM.ipynb                 # LSTM training/evaluation notebook
└── DDoS_Detection(Models_Comparison).ipynb   # SVM vs CNN vs LSTM comparison notebook
```

## Model

- **Architecture:** `LSTM(64, return_sequences=True) → Dropout(0.3) → LSTM(32) → Dropout(0.3) → Dense(1, sigmoid)`
- **Input:** 81 flow-level features per sample, reshaped to `(1, 1, 81)` for the LSTM
- **Output:** Probability of the traffic being part of a DDoS attack
- **Training data:** Flow features from a CIC-DDoS2019-style dataset (`Portmap.csv`), with labels normalized to binary (benign vs. attack)
- **Preprocessing:** Features are standardized with `sklearn.StandardScaler` (saved as `scaler.pkl`) before being passed to the model

The comparison notebook also trains an SVM and a CNN on the same data as baselines against the LSTM.

## Requirements

- Python 3.9+
- [Wireshark](https://www.wireshark.org/) / `tshark` installed and on your `PATH` (required by `pyshark` for live capture)
- Npcap/libpcap with permissions to capture on a network interface (may require running as Administrator/root)

Install the Python dependencies:

```bash
pip install tensorflow flask flask-socketio python-socketio pyshark scapy scikit-learn joblib pandas numpy matplotlib seaborn
```

## Usage

### 1. Start the detection server

```bash
python app.py
```

This starts the Flask-SocketIO server on `http://127.0.0.1:5000` and serves the live dashboard at that address.

### 2. (Optional) Start the mock victim server

```bash
python victime_site.py
```

Runs a sample "bank" landing page on `http://127.0.0.1:8080` that you can use as a target for local attack simulation.

### 3. Start the sniffer

```bash
python sniffer.py
```

Update the `IFACE` variable in `sniffer.py` to match the name of the interface you want to capture on (e.g. your loopback adapter for local testing, as reported by Wireshark/`tshark -D`). The sniffer extracts features from live packets and streams them to `app.py` over Socket.IO.

### 4. View the dashboard

Open `http://127.0.0.1:5000` in your browser to watch real-time traffic load and threat alerts.

### 5. (Optional) Simulate an attack

```bash
python attack.py
```

Sends a continuous stream of TCP SYN packets to `127.0.0.1:8080` to simulate a flood. Watch the dashboard flip into an alert state as the model's rolling average attack probability crosses the detection threshold.

## Notebooks

| Notebook | Purpose |
|---|---|
| `DDoS_LSTM.ipynb` | End-to-end LSTM training: preprocessing, model build, training curves, evaluation, and inference on new samples |
| `DDoS_Detection_LSTM.ipynb` | Additional LSTM training/evaluation pass |
| `DDoS_Detection(Models_Comparison).ipynb` | Trains SVM, CNN, and LSTM on the same dataset and compares their accuracy |

## Notes & limitations

- The feature vector produced by `sniffer.py` is a simplified subset (packet length, protocol, ports, TCP window size, SYN flag) padded with placeholder values, and does not fully match the rich flow-level features used at training time — treat the live demo as a proof of concept rather than a production-accurate detector.
- The detection threshold (`avg_prob > 0.85` over the last 10 packets) is tuned for the demo and may need adjustment for other environments or datasets.
- Capturing live traffic typically requires elevated/administrator privileges.

## License

No license specified. Add a `LICENSE` file if you intend to share or reuse this code.
