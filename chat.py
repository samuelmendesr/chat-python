import sys, threading, socket, pickle

class listen(threading.Thread):
    def __init__(self, sock, host):
        threading.Thread.__init__(self)
        self.sock = sock
        self.host = host
        self.connection = True
    def run(self):
        while self.connection:
            data = self.sock.recv(1024)
            msg = pickle.loads(data)
            
            if msg[0] == 'close':
                msg[0] = 'close_reply'
                data = pickle.dumps(msg)
                self.sock.send(data)
                self.connection = False
                print(self.host, "closed the connection, press any key")
            elif msg[0] == 'close_reply':
                self.connection = False
            else:
                print("[", self.host, "]:", msg[1])
        
        self.sock.close()

try:
    target_host = input("connect: ")
    target_port = 50000

    if target_host:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target_host, target_port))
    else:
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.bind((target_host, target_port))
        server_sock.listen(1)

        print("waiting...")

        sock, client = server_sock.accept()
        target_host = client[0]
        
except KeyboardInterrupt:
    sys.exit()
    
except socket.error as exc:
    print("Connection error:", exc)
    sys.exit()

t_listen = listen(sock, target_host)
t_listen.start()

print("Connection established with", target_host)

msg = ['tag','msg']

try:
    while True:
        msg[1] = input()
        if not t_listen.connection: 
            break
        if msg[1]:
            data = pickle.dumps(msg)
            sock.send(data)
        
except KeyboardInterrupt:
    msg[0] = 'close'
    data = pickle.dumps(msg)
    sock.send(data)

t_listen.join()
print("\nEnd of connection with", target_host)
