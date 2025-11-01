import socket
import os
import json
import time
import select

def get_local_ip():
    """Get the local IP address of this machine."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
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
        metadata = {'type': 'file', 'name': file_name, 'size': file_size}
        conn.send(json.dumps(metadata).encode('utf-8'))
        conn.recv(1024)

        with open(file_path, 'rb') as file:
            while True:
                data = file.read(4096)
                if not data:
                    break
                conn.sendall(data)
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
        with open(file_name, 'wb') as f:
            while received_size < file_size:
                data = conn.recv(4096)
                if not data:
                    break
                f.write(data)
                received_size += len(data)
        print(f"✅ File '{file_name}' received successfully!")
    except Exception as e:
        print(f"❌ Error receiving file: {e}")


def handle_chat(conn):
    """Handle chat messages"""
    while True:
        try:
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

            # Reply
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

        except ConnectionResetError:
            print("⚠️ Connection lost.")
            break
        except KeyboardInterrupt:
            print("\n👋 Server interrupted during chat.")
            break


def start_server():
    port = 12345
    local_ip = get_local_ip()
    host = "0.0.0.0"

    # with open("server_ip.txt", "w") as f:
    #     f.write(local_ip)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)
    server_socket.setblocking(False)  # ✅ Non-blocking mode

    print("🚀 Server started!")
    print(f"🌐 Your IP address: {local_ip}")
    print(f"📡 Clients should connect using port {port}")
    print("💬 Commands: /sendfile /quit")
    print("⏳ Waiting for connection (Ctrl+C to stop)...")

    conn = None
    try:
        while True:
            try:
                readable, _, _ = select.select([server_socket], [], [], 0.5)
                if readable:
                    conn, addr = server_socket.accept()
                    print(f"✅ Connected to {addr}")
                    handle_chat(conn)
                    break
                # Small sleep to reduce CPU usage
                time.sleep(0.1)
            except KeyboardInterrupt:
                print("\n👋 Server interrupted. Shutting down.")
                break
            except Exception:
                time.sleep(0.1)
                continue
    finally:
        if conn:
            conn.close()
        server_socket.close()
        print("👋 Server closed")


if __name__ == "__main__":
    start_server()
