import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip, port = "120.27.162.128", 12500
sock.connect((ip, port))


def accept(sock: socket.socket):
    rc = sock.recv(65535)
    while rc != b'':
        print("accept from", sock, ":", rc.decode('utf-8'))
        rc = sock.recv(65535)


th = threading.Thread(target=accept, args=(sock,))
th.start()
inp = input()
while inp != "!":
    try:
        sock.send(inp.encode('utf-8'))
        print("send success")
    except Exception as e:
        print(e)
        print("connect break")
        break
    inp = input()
