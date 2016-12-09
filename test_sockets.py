import socket
sock = socket.socket()
порт = 3228
sock.connect(("127.0.0.1", порт)) 
data = b'lol'
while True:
    s = input()
    if s == 'exit':
        break
    sock.send(s.encode())
    print(str(sock.recv(1024), encoding = 'ascii'))
sock.close()
