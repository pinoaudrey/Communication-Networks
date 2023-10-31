# Team Members: Audrey Pino & Tony Czajka
import socket
import struct
import os

SAVE_DIR = 'received_files'

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def main(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('0.0.0.0', port))

    # Receive file size and name
    data, addr = s.recvfrom(24)
    file_size = struct.unpack('!I', data[:4])[0]
    file_name = data[4:].decode().strip()

    file_path = os.path.join(SAVE_DIR, file_name)

    with open(file_path, 'wb') as f:
        while file_size > 0:
            chunk, _ = s.recvfrom(1024)
            f.write(chunk)
            file_size -= len(chunk)

    print(f"File received and saved as {file_path}")
    s.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 UDP-server.py <local-port>")
        sys.exit(1)

    port = int(sys.argv[1])
    main(port)
