import socket 
import threading
import struct
import os

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
        
        operation = conn.recv(4) #recieves 4 byte UINT
        operation = struct.unpack('<I', operation)[0]
        #forgive me for what i'm about to write (why does python not have a switch statement? for multithreaded stuff like this dictionarys with methods seems painful)
        if (operation == 1): #send file to client
            f = open('test.dll', 'rb') #the name of the file to send in current directory
            fileSize = os.fstat(f.fileno()).st_size
            conn.send(struct.pack('<I', fileSize)) #turns filesize into an Int so c/c++ can read it normally

            chunkCount = fileSize // 2000
            remainingBytes = fileSize % 2000

            i = 0
            while i < chunkCount:
                conn.send(f.read(2000))
                i+=1

            if remainingBytes > 0:
                #send rest of data
                conn.send(f.read(remainingBytes))

            f.close()
            
        elif (operation == 2): #recieve string message from client
            msg_length = conn.recv(4)
            msg_length = struct.unpack('<i', msg_length)[0]

            msg = conn.recv(msg_length).decode(FORMAT) 
            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))
            
        elif (operation == 3): #end connection operation from client
            connected = False

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
