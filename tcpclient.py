import socket
import time

def send_heartbeat():
    # Define server address and port
    server_address = ("192.168.20.192", 5001)
    
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the server
        client_socket.connect(server_address)
        print(f"Connected to server at {server_address}")

        # Send periodic "heartbeat" messages
        while True:
            message = b'heartbeat'  # Message content (could be anything)
            client_socket.sendall(message)  # Send message over TCP
            print("Sent heartbeat")
            time.sleep(1)  # Send every 1 second
    except KeyboardInterrupt:
        print("Client stopped.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

# Start sending heartbeat
send_heartbeat()
