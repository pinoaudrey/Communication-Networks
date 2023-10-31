# Team Members: Audrey Pino & Tony Czajka
import socket
import struct
import os

def main(ip, port, file_path):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)

    if len(file_name) > 20:
        print("File name too long!")
        s.close()
        return

    # Send file size and name
    s.sendto(struct.pack('!I', file_size) + file_name.ljust(20).encode(), (ip, port))

    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(1024)
            if not chunk:
                break
            s.sendto(chunk, (ip, port))

    print(f"File {file_path} sent!")
    s.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python3 UDP-client.py <remote-IP> <remote-port> <local-file-path>")
        sys.exit(1)

    remote_ip = sys.argv[1]
    remote_port = int(sys.argv[2])
    file_path = sys.argv[3]
    main(remote_ip, remote_port, file_path)
