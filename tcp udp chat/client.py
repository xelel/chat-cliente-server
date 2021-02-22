import socket
import threading
import random
import os


def tcpclient():

    nickname = input("Choose your nickname: ")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5008))

    def receive():
        while True:
            try:

                message = client.recv(1024).decode('ascii')
                if message == 'NICK':
                    client.send(nickname.encode('ascii'))
                else:
                    print(message)
            except:

                print("An error occured!")
                client.close()
                break

    def write():
        while True:
            data = input()

            message = '{}: {}'.format(nickname, data)

            client.send(message.encode('ascii'))

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()


def udpClient():
    # Client Code
    def ReceiveData(sock):
        while True:
            try:
                data, addr = sock.recvfrom(1024)
                print(data.decode('utf-8'))
            except:
                pass

    def RunClient(serverIP):
        host = socket.gethostbyname(socket.gethostname())
        port = random.randint(6000, 10000)
        print('Client IP->' + str(host) + ' Port->' + str(port))
        server = (str(serverIP), 5000)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((host, port))

        name = input('Choose your Nickname: ')
        if name == '':
            name = 'Guest' + str(random.randint(1000, 9999))
            print('Nickname:' + name)
        s.sendto(name.encode('utf-8'), server)
        threading.Thread(target=ReceiveData, args=(s,)).start()
        while True:

            data = input()
            if data == 'quit':
                break
            elif data == '':
                continue
            data = '[' + name + ']' + ' : ' + data
            s.sendto(data.encode('utf-8'), server)
        s.sendto(data.encode('utf-8'), server)
        s.close()
        os._exit(1)

    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    RunClient(local_ip)


if __name__ == '__main__':

    prot = str(input('Escolha o protocolo à ser executado no cliente(udp/tcp):'))
    if prot == 'udp':
        print('Protocolo UDP está sendo executado')
        udpClient()
    else:
        print('Protocolo TCP está sendo executado')
        tcpclient()
