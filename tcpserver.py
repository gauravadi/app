import socket
import threading
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Set to track active clients' IPs and manage connections
connected_clients = set()
client_sockets = {}

# TCP server function to handle client communication
def start_tcp_server():
    # Start TCP server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("192.168.20.192", 5001))
    server_socket.listen(5)
    print("TCP server running on port 5001")

    while True:
        client_socket, client_address = server_socket.accept()  # Accept new client connection
        print(f"New client connected from {client_address}")
        
        # Add client and its socket to tracking structures
        if client_address not in connected_clients:
            connected_clients.add(client_address)
            client_sockets[client_address] = client_socket

        # Start a new thread to handle this client
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

def handle_client(client_socket, client_address):
    try:
        while True:
            # Receive heartbeat message
            message = client_socket.recv(1024)
            if not message:
                break  # Disconnect if no message is received

            # Only heartbeat messages are expected, so just update client data
            broadcast_client_data()
    except Exception as e:
        print(f"Client {client_address} disconnected with error: {e}")
    finally:
        # Remove client on disconnect
        connected_clients.discard(client_address)
        client_sockets.pop(client_address, None)
        client_socket.close()
        broadcast_client_data()

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
    # Start the TCP server in a separate thread
    tcp_thread = threading.Thread(target=start_tcp_server)
    tcp_thread.start()
    
    # Start the Flask WebSocket server
    socketio.run(app, port=5000)
