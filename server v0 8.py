import os
import sys
import select
import socket
import threading
ip_address = '127.0.0.1'
port = int(sys.argv[1])

def get_method(method):
    if method in ['get','GET']:
        print ("The method asked by the client is Get method")
    elif method in ['post','POST']:
        print ("POST method is not implemented as part of this")
    else:
        print ("Bad request by client")


def get_version(http_version):
    if http_version is 'HTTP/1.0':
        version = 1.0
    else:
        version = 1.1


def get_root_directory():
    file = open("httpd.txt","r")
    lines = file.readlines()
    for line in lines:
        if line.startswith('ROOT_DIRECTORY'):
            directory = line.split()
    file.close()
    root_directory = directory[1]
    if not os.path.exists(root_directory):
        print ("There is no such root directory which you have mentioned in the httpd file")
        sys.exit()
    return root_directory

def send_error_client(buff,conn):
    if buff:
        conn.send(bytes(buff, 'utf-8'))
        conn.send(bytes('<http><h1>HTTP Error 404</h1><i>The requested page is not found</i></html>','utf-8'))


def error_handling(code, conn):
    if code == 404:
        data = 'HTTP/1.0 404 Not Found\r\n\r\n'
    send_error_client(data, conn)
    conn.close()
    
def file_path_exists(filename):
    if os.path.isfile(filename):
        file_exists = True
    else:
        file_exists = False
    return file_exists


def read_file(fpath):
    f = open(fpath,"rb")
    data = f.read()
    f.close()
    return data

def send_file(buff, conn):
    if buff:
        conn.send(bytes('HTTP/1.0 200 OK\r\n\r\n', 'utf-8'))
        conn.send(buff)
    

def get_file_path(file_name, conn):
    root_dir = get_root_directory()
    if file_name == '/':
        file_name = file_name.replace('/','index.html')
    elif file_name.startswith('/') and file_name.endswith('.html'):
        file_name = file_name.replace('/',"")
    file_path = os.path.join(root_dir,file_name)
    value = file_path_exists(file_path)
    if value == False:
        code = 404
        error_handling(code, conn)
    else:
        data = read_file(file_path)
        send_file(data, conn)
        conn.close()



sock_list = []
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print ('socket created')
s.bind((ip_address,port))
s.listen(10)
sock_list.append(s)
print (threading.active_count())
while(1):
    try:
        read_sock,write_sock,error_sock = select.select(sock_list,[],[],2)
    except ValueError:
        pass
    for sock in read_sock:
        if sock == s:
            conn,addr = s.accept()
            sock_list.append(conn)
        else:
            recieved_string = (sock.recv(1024)).decode(encoding = 'UTF-8')
            data = recieved_string.split()
            get_method(data[0])
            get_version(data[2])
            print ("The client's port is:", addr[1])
            if data[1].startswith('/') and data[1].endswith('.ico'):
                sock.close()
                sock_list.remove(sock)
                continue
            else:
                get_file_path(data[1], sock)
                sock_list.remove(sock)
s.close()
