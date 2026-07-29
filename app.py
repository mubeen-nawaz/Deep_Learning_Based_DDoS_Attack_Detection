import numpy as np
import joblib
from flask import Flask, render_template
from flask_socketio import SocketIO
from tensorflow.keras.models import load_model

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

model = load_model('lstm_ddos_model.h5')
scaler = joblib.load('scaler.pkl')

# Memory to track recent predictions (to avoid one-packet false alarms)
prediction_history = []

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('packet_data')
def handle_packet(data):
    global prediction_history
    try:
        features = np.array(data['features']).reshape(1, -1)
        # Ensure data is scaled correctly
        scaled = scaler.transform(features)
        lstm_input = scaled.reshape((1, 1, 81))
        
        prob = model.predict(lstm_input, verbose=0)[0][0]
        
        # Add to history (keep last 10 packets)
        prediction_history.append(prob)
        if len(prediction_history) > 10:
            prediction_history.pop(0)

        # TRIGGER LOGIC: Only alert if the AVERAGE of recent packets is high
        avg_prob = sum(prediction_history) / len(prediction_history)
        is_attack = avg_prob > 0.85 # High confidence over multiple packets

        payload = {
            'prediction': "DDoS" if is_attack else "Normal",
            'probability': float(prob),
            'avg_prob': float(avg_prob),
            'src_ip': data.get('src_ip')
        }

        if is_attack:
            socketio.emit('ddos_alert', payload)
        else:
            socketio.emit('traffic_update', payload)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    socketio.run(app, port=5000)