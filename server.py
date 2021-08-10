import socket 
import threading
import struct

HEADER = 16
PORT = 6969
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

serverRunning = True

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER) #.decode(FORMAT)
        if msg_length:
            unpack_len = msg_length.decode(FORMAT) #struct.unpack('!s', msg_length)[0].
            msg_length = int(unpack_len)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                global serverRunning
                serverRunning = False
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))
    conn.close()
    
    
    
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")

    while serverRunning:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()
