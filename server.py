import socket
import threading
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Dictionary to track active clients' IPs
connected_clients = set()

# UDP server function to handle client communication
def start_udp_server():
    # Start UDP server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("192.168.20.192", 5001))
    print("UDP server running on port 5001")

    while True:
        message, client_address = server_socket.recvfrom(1024)  # Receive messages
        if client_address not in connected_clients:
            connected_clients.add(client_address)  # Add new client
        broadcast_client_data()  # Broadcast updated client data

        # In UDP, there's no need to keep the connection open, so no need to handle disconnections explicitly.

def broadcast_client_data():
    client_data = {
        "count": len(connected_clients),
        "clients": [f"{client[0]}:{client[1]}" for client in connected_clients]
    }
    # Send data to all connected WebSocket clients
    socketio.emit('client_update', client_data)

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    # Start the UDP server in a separate thread
    udp_thread = threading.Thread(target=start_udp_server)
    udp_thread.start()
    
    # Start the Flask WebSocket server
    socketio.run(app, port=5000)
