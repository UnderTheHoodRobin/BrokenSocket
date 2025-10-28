import socket
import os
import json


def get_local_ip():
    """Get the local IP address of this machine."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Connect to a dummy external address
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def send_file(conn, file_path):
    """Send a file to the client"""
    try:
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)

        # Send file metadata
        metadata = {'type': 'file', 'name': file_name, 'size': file_size}
        conn.send(json.dumps(metadata).encode('utf-8'))

        # Wait for client ready
        conn.recv(1024)

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
    """Receive a file from the client"""
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


def handle_chat(conn):
    """Handle chat messages"""
    while True:
        data = conn.recv(1024).decode('utf-8')
        if not data:
            break

        if data.startswith('/'):
            if data == '/sendfile':
                receive_file(conn)
            elif data == '/quit':
                break
            else:
                print(f"❌ Unknown command: {data}")
        else:
            print(f"📱 Client: {data}")

        # Server reply
        response = input("💻 You: ")

        if response.startswith('/'):
            if response == '/sendfile':
                file_path = input("Enter file path to send: ")
                if os.path.exists(file_path):
                    conn.send(b'/sendfile')
                    send_file(conn, file_path)
                else:
                    print("❌ File not found!")
                    conn.send(b"File not found")
            elif response == '/quit':
                conn.send(b'/quit')
                break
            else:
                conn.send(f"Unknown command: {response}".encode('utf-8'))
        else:
            conn.send(response.encode('utf-8'))


def start_server():
    port = 12345
    local_ip = get_local_ip()
    host = "0.0.0.0"

    # Save IP for future client use
    with open("server_ip.txt", "w") as f:
        f.write(local_ip)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("🚀 Server started!")
    print(f"🌐 Your IP address: {local_ip}")
    print(f"📡 Clients should connect using this IP and port {port}")
    print("💬 Chat commands:")
    print("   /sendfile - Send or receive files")
    print("   /quit - Exit")
    print("⏳ Waiting for connection...")

    conn, addr = server_socket.accept()
    print(f"✅ Connected to {addr}")

    try:
        handle_chat(conn)
    except Exception as e:
        print(f"❌ Connection error: {e}")
    finally:
        conn.close()
        server_socket.close()
        print("👋 Server closed")


if __name__ == "__main__":
    start_server()
