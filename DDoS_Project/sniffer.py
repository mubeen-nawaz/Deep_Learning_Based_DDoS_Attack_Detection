import pyshark
import socketio

sio = socketio.Client()
sio.connect('http://127.0.0.1:5000')

IFACE = 'Adapter for loopback traffic capture' 

def start_sniffing():
    print(f"[*] Monitoring {IFACE}...")
    capture = pyshark.LiveCapture(interface=IFACE, display_filter="ip")

    for packet in capture.sniff_continuously():
        try:
            features = [0.01] * 81 
            
            features[0] = float(packet.length)
            features[1] = float(packet.ip.proto)
            
            if 'TCP' in packet:
                features[2] = float(packet.tcp.srcport)
                features[3] = float(packet.tcp.dstport)
                features[4] = float(packet.tcp.window_size)
                if 'S' in packet.tcp.flags: features[5] = 1.0
            
            sio.emit('packet_data', {
                'features': features,
                'src_ip': packet.ip.src
            })
        except: continue

if __name__ == "__main__":
    start_sniffing()