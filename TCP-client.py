import socket
import struct
import os

def main(ip, port, file_path):
    # Create TCP socket and connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))

    # Get the size and name of the file
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)
    
    # Ensure the file name fits within 20 bytes
    if len(file_name) > 20:
        print("File name too long!")
        s.close()
        return

    # Send file size (4 bytes) and file name (20 bytes)
    s.sendall(struct.pack('!I', file_size))
    s.sendall(file_name.ljust(20).encode())

    # Send the file data
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(1024)
            if not chunk:
                break
            s.sendall(chunk)

    print(f"File {file_path} sent!")
    s.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python3 TCP-client.py <remote-IP> <remote-port> <local-file-path>")
        sys.exit(1)
    
    remote_ip = sys.argv[1]
    remote_port = int(sys.argv[2])
    file_path = sys.argv[3]
    main(remote_ip, remote_port, file_path)
