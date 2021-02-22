import socket
import threading
import queue
import sys
import random
import os

def tcpServer():
    host = '127.0.0.1'
    port = 5008

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    clients = []
    nicknames = []


    def broadcast(message):
        for client in clients:
            client.send(message)


    def handle(client):
        while True:
            try:

                message = client.recv(1024)
                print(message.decode('ascii'))
                broadcast(message)
            except:

                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast('{} left!'.format(nickname).encode('ascii'))
                nicknames.remove(nickname)
                break

    def receive():
        while True:

            client, address = server.accept()
            print("Connected with {}".format(str(address)))


            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            nicknames.append(nickname)
            clients.append(client)


            print("Nickname is {}".format(nickname))
            broadcast("{} joined!".format(nickname).encode('ascii'))

            client.send('Connected to server!'.encode('ascii'))


            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
    print('Server is listening....')
    receive()

def udpServer():
    def RecvData(sock, recvPackets):
        while True:
            data, addr = sock.recvfrom(1024)
            recvPackets.put((data, addr))


    def RunServer():
        host = socket.gethostbyname(socket.gethostname())
        port = 5000
        print('Server hosting on IP-> ' + str(host))
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((host, port))
        clients = set()
        recvPackets = queue.Queue()

        print('Server is listening...')

        threading.Thread(target=RecvData, args=(s, recvPackets)).start()

        while True:
            while not recvPackets.empty():
                data, addr = recvPackets.get()
                if addr not in clients:
                    clients.add(addr)
                    continue
                clients.add(addr)
                data = data.decode('utf-8')
                if data.endswith('qqq'):
                    clients.remove(addr)
                    continue
                print(str(addr) + data)
                for c in clients:
                        s.sendto(data.encode('utf-8'), c)
        s.close()


    RunServer()

if __name__=='__main__':
    prot=str(input('Escolha o prótocolo do chat: (udp/tcp)'))
    if prot=='udp':
        udpServer()
    else:
        print('Protocolo TCP está sendo executado, inicialize o cliente TCP')
        tcpServer()