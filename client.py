import socket
import time

def send_heartbeat():
    # Define server address and port
    server_address = ("192.168.20.192", 5001)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Send periodic "heartbeat" messages
    try:
        while True:
            message = b'heartbeat'  # Message content (could be anything)
            client_socket.sendto(message, server_address)  # Send to server
            print(f"Sent heartbeat to {server_address}")
            time.sleep(1)  # Send every 1 second
    except KeyboardInterrupt:
        print("Client stopped.")
    finally:
        client_socket.close()

# Start sending heartbeat
send_heartbeat()
