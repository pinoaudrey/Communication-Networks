Team Members: Audrey Pino & Tony Czajka
import socket
import struct
import os

# Directory where the received files will be saved
SAVE_DIR = 'received_files'

# Check if SAVE_DIR exists or not, if not create it
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def main(port):
    # Create TCP socket and bind it to the provided port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    s.listen(1)
    print(f"Listening on port {port}")

    conn, addr = s.accept()
    print(f"Connection from {addr}")

    # Receive the first 4 bytes for the file size
    file_size_data = conn.recv(4)
    file_size = struct.unpack('!I', file_size_data)[0]

    # Receive the next 20 bytes for the file name
    file_name_data = conn.recv(20)
    file_name = file_name_data.decode().strip()

    # Create a file path for saving
    file_path = os.path.join(SAVE_DIR, file_name)

    # Start receiving the file data
    with open(file_path, 'wb') as f:
        while file_size > 0:
            chunk = conn.recv(1024)
            if not chunk:
                break
            f.write(chunk)
            file_size -= len(chunk)

    print(f"File received and saved as {file_path}")
    conn.close()
    s.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 TCP-server.py <local-port>")
        sys.exit(1)
    
    port = int(sys.argv[1])
    main(port)
