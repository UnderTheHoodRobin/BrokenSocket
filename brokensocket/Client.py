import socket
import os
import json


def send_file(conn, file_path):
    """Send a file to the server"""
    try:
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)

        metadata = {'type': 'file', 'name': file_name, 'size': file_size}
        conn.send(json.dumps(metadata).encode('utf-8'))

        conn.recv(1024)  # Wait for READY

        with open(file_path, 'rb') as file:
            total_sent = 0
            while total_sent < file_size:
                data = file.read(4096)
                conn.send(data)
                total_sent += len(data)

        print(f"✅ File '{file_name}' sent successfully!")

    except Exception as e:
        print(f"❌ Error sending file: {e}")


def receive_file(conn):
    """Receive a file from the server"""
    try:
        metadata = json.loads(conn.recv(1024).decode('utf-8'))
        file_name = metadata['name']
        file_size = metadata['size']

        print(f"📥 Receiving file: {file_name} ({file_size} bytes)")
        conn.send(b'READY')

        received_size = 0
        with open(file_name, 'wb') as file:
            while received_size < file_size:
                data = conn.recv(4096)
                if not data:
                    break
                file.write(data)
                received_size += len(data)

        print(f"✅ File '{file_name}' received successfully!")

    except Exception as e:
        print(f"❌ Error receiving file: {e}")


def get_server_ip():
    """Load or ask for the server IP"""
    # ip_file = "server_ip.txt"
    # if os.path.exists(ip_file):
    #     with open(ip_file, "r") as f:
    #         saved_ip = f.read().strip()
    #     use_saved = input(f"Use saved server IP ({saved_ip})? [Y/n]: ").strip().lower()
    #     if use_saved in ("", "y", "yes"):
    #         return saved_ip
    return input("Enter server IP address: ").strip()


def start_client():
    port = 12345
    server_ip = get_server_ip()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))

    print(f"✅ Connected to server at {server_ip}:{port}")
    print("💬 Chat commands:")
    print("   /sendfile - Send or receive files")
    print("   /quit - Exit")

    try:
        while True:
            message = input("📱 You: ")

            if message.startswith('/'):
                if message == '/sendfile':
                    client_socket.send(b'/sendfile')
                    file_path = input("Enter file path to send: ")
                    if os.path.exists(file_path):
                        send_file(client_socket, file_path)
                    else:
                        print("❌ File not found!")
                        client_socket.send(b"File not found")
                elif message == '/quit':
                    client_socket.send(b'/quit')
                    break
                else:
                    client_socket.send(message.encode('utf-8'))
            else:
                client_socket.send(message.encode('utf-8'))

            data = client_socket.recv(1024).decode('utf-8')
            if data == '/sendfile':
                receive_file(client_socket)
            elif data.lower() == '/quit':
                break
            else:
                print(f"💻 Server: {data}")

    except Exception as e:
        print(f"❌ Connection error: {e}")
    finally:
        client_socket.close()
        print("👋 Disconnected")


if __name__ == "__main__":
    start_client()