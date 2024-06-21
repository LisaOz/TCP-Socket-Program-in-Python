import socket
import logging
import threading


# Configure logging to a shared log file
logging.basicConfig(filename='communication.log', level=logging.INFO, format='%(asctime)s - %(message)s')


def handle_client(client_socket, client_address):
    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break # Connection is closed if there are no messages

            # Process received data
            logging.info("Received from {}: {}".format(client_address, data.decode('utf-8')))

            # Send response back to client
            client_socket.sendall(b"RESPONSE FROM SERVER")
    except Exception as e:
        # Print and log the error message if the server fails to start
        print("Error receiving messages from clients:", e)
        logging.error(f"Error during communication with {client_address}: {e}")
    finally:
        # Close the client socket
        client_socket.close()
        print(f"Connection with {client_address} closed.")

def run_server(ip_address, port):
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Bind the socket to an IP address and port
        server_socket.bind((ip_address, port))  # bind method used to assign the ip address and a port as a tuple

        # Listen for incoming connections
        server_socket.listen()
        print("TCP SERVER STARTED, WAITING FOR CONNECTIONS...")

        while True:
            # Receive a connection from a client
            client_socket, client_address = server_socket.accept()
            print("Connected to client:", client_address)

            # Create a new thread to handle the client
            client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_handler.start()
    except Exception as e:
        print("Error while running the server:", e)
        logging.error("Error while running the server: %s", e)

    finally:
        # Close the server socket
        server_socket.close()


if __name__ == "__main__":
    # Connecting to the Localhost
    ip_address = '127.0.0.1'
    port = 5555       # port range 1 to 65535

    # Run the server
    run_server(ip_address, port)


