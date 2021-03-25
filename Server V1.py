import socket, os, subprocess, shutil, pickle, struct, threading
## gettig the hostname by socket.gethostname() method
hostname = socket.gethostname()
## getting the IP address using socket.gethostbyname() method
ip_address = socket.gethostbyname(hostname)

# Create a Socket ( connect two computers)

def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        create_socket()


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        s.bind((host, port))
        s.listen(5)
        ## printing the hostname and ip_address
        print(f"Hostname: {hostname}")
        print(f"IP Address: {ip_address}")
        print(f"Running Port: {port}")
    except socket.error as msg:
        bind_socket()
        print(bind_socket())


# send file list

def flist(conn):
    try:
        arr = pickle.dumps(os.listdir())
        conn.send(arr)
        print(arr)
    except:
        conn.send(('Error').encode("utf-8"))


# accept file from server

def fdown(filename, conn):
    try:
        data = conn.recv(1024).decode("utf-8")
        if data[:6] == 'EXISTS':
            filesize = data[6:]
            conn.send("OK".encode("utf-8"))
            f = open(filename, 'wb')
            data = (conn.recv(1024))
            totalRecv = len(data)
            f.write(data)
            while int(totalRecv) < int(filesize):
                data = conn.recv(1024)
                totalRecv += len(data)
                f.write(data)
            f.close()
    except:
        conn.send(('Error').encode("utf-8"))


# send file

def fup(filename, conn):
    if os.path.isfile(filename):
        conn.send(str.encode("EXISTS " + str(os.path.getsize(filename))))
        filesize = int(os.path.getsize(filename))
        userResponse = conn.recv(1024).decode("utf-8")
        if userResponse[:2] == 'OK':
            with open(filename, 'rb') as f:
                bytesToSend = f.read(1024)
                conn.send(bytesToSend)
                totalSend = len(bytesToSend)
                while int(totalSend) < int(filesize):
                    bytesToSend = f.read(1024)
                    totalSend += len(bytesToSend)
                    conn.send(bytesToSend)
    else:
        conn.send("ERROR".encode("utf-8"))


# main
def main(s):
    while True:
        data = (s.recv(1024)).decode("utf-8").split('~')
        if data[0] == 'fdown':
            fup(data[1], s)
        elif data[0] == 'fup':
            fdown(data[1], s)
        elif data[0] == 'flist':
            flist(s)
        else:
            s.send(".".encode('utf-8'))


def socket_accept():
    while True:
        conn, address = s.accept()
        t = threading.Thread(target=main, args=(conn,))
        t.start()


create_socket()
bind_socket()
socket_accept()










