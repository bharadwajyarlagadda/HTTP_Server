import os
import math
import sys
import resource
import time
import select
import timeit
import socket
import threading

ip_address = 'localhost'
port = int(sys.argv[1])
thread_lock = threading.Lock()

class http_one_zero(threading.Thread):
    def __init__(self, args = ()):
        threading.Thread.__init__(self)
        self.conn = sock
        self.root_dir = root_dir
        self.file_name = file_name
        self.method = method
        self.http_version = http_version
        self.data = ''

    def run(self):
        self.recv_data()
        '''print ("The client's port is:", self.conn)'''
        if self.file_name.startswith('/') and self.file_name.endswith('.ico'):
            self.send_quit_to_client()
        else:
            self.get_file_path()

    def recv_data(self):
        print ("the method asked by the client is:", self.method)
        print ("the http version asked by the client is:", self.http_version)

    def get_file_path(self):
        if self.file_name == '/':
            self.file_name = self.file_name.replace('/','index.html')
        elif self.file_name.startswith('/') and self.file_name.endswith('.html'):
            self.file_name = self.file_name.replace('/',"")
        file_path = os.path.join(self.root_dir,self.file_name)
        value = self.file_path_exists(file_path)
        if value == False:
            code = 404
            self.error_handling(code)
        else:
            self.data = self.read_file(file_path)
            self.send_file()

    def send_quit_to_client(self):
        data_quit = 'QUIT'
        self.conn.send(bytes(data_quit,'utf-8'))
        print ("Closing the connection")
        self.conn.close()

    def send_file(self):
        if self.data:
            self.conn.send(bytes('HTTP/1.0 200 OK\r\n\r\n','utf-8'))
            self.conn.send(self.data)
        self.send_quit_to_client()

    def error_handling(self, code):
        if code == 404:
            data = 'HTTP/1.0 404 Not Found\r\n\r\n'
        self.send_error_client(bytes(data,'utf-8'))
        self.send_quit_to_client()

    def read_file(self, fpath):
        f = open(fpath,"rb")
        data = f.read()
        f.close()
        return data

    def file_path_exists(self, filename):
        if os.path.isfile(filename):
            file_exists = True
        else:
            file_exists = False
        return file_exists

    def send_error_client(self, buff):
        if buff:
            self.conn.send(buff)
            self.conn.send(bytes('<http><h1>HTTP Error 404</h1><i>The requested page is not found</i></html>','utf-8'))

class http_one_one(threading.Thread):
    def __init__(self, args = ()):
        threading.Thread.__init__(self)
        self.conn = sock
        self.root_dir = root_dir
        self.file_name = file_name
        self.method = method
        self.http_version = http_version
        self.data = ''

    def run(self):
        self.recv_data()
        '''print ("The client's port is:", self.conn)'''
        if self.file_name.startswith('/') and self.file_name.endswith('.ico'):
            self.send_quit_to_client()
        else:
            self.get_file_path()

    def recv_data(self):
        print ("the method asked by the client is:", self.method)
        print ("the http version asked by the client is:", self.http_version)

    def get_file_path(self):
        if self.file_name == '/':
            self.file_name = self.file_name.replace('/','index.html')
        elif self.file_name.startswith('/') and self.file_name.endswith('.html'):
            self.file_name = self.file_name.replace('/',"")
        file_path = os.path.join(self.root_dir,self.file_name)
        value = self.file_path_exists(file_path)
        if value == False:
            code = 404
            self.error_handling(code)
        else:
            self.data = self.read_file(file_path)
            self.send_file()

    def send_quit_to_client(self):
        data_quit = 'QUIT'
        self.conn.send(bytes(data_quit,'utf-8'))

    def send_file(self):
        if self.data:
            self.conn.send(bytes('HTTP/1.1 200 OK\r\n\r\n','utf-8'))
            self.conn.send(self.data)
        self.send_quit_to_client()

    def error_handling(self, code):
        if code == 404:
            data = 'HTTP/1.1 404 Not Found\r\n\r\n'
        self.send_error_client(bytes(data,'utf-8'))
        time.sleep(4)
        self.send_quit_to_client()

    def read_file(self, fpath):
        f = open(fpath,"rb")
        data = f.read()
        f.close()
        return data

    def file_path_exists(self, filename):
        if os.path.isfile(filename):
            file_exists = True
        else:
            file_exists = False
        return file_exists

    def send_error_client(self, buff):
        if buff:
            self.conn.send(buff)
            self.conn.send(bytes('<http><h1>HTTP Error 404</h1><i>The requested page is not found</i></html>','utf-8'))


        

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
        

if "__main__" == __name__:
    root_dir = get_root_directory()
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print ('socket created')
    s.bind((ip_address,port))
    s.listen(1100)
    threads = []
    sock_list = []
    sock_list.append(s)
    try:
        while(1):
            try:
                read_sock,write_sock,error_sock = select.select(sock_list,[],[],1)
            except ValueError:
                pass
            for sock in read_sock:
                if sock == s:
                    conn,addr = s.accept()
                    sock_list.append(conn)
                else:
                    recieved_string = (conn.recv(1024)).decode(encoding = 'UTF-8')
                    print(recieved_string)
                    if recieved_string.endswith('QUIT'):
                        conn.close
                        sock_list.remove(sock)
                    else:
                        data = recieved_string.split()
                        file_name = data[1]
                        if data[0] in ['get','GET']:
                            method = data[0]
                        elif data[0] in ['post','POST']:
                            method = data[0]
                        else:
                            method = data[0]
                        if data[2] == 'HTTP/1.0':
                            http_version = 1.0
                        else:
                            http_version = 1.1
                        if http_version == 1.0:
                            new_thread = http_one_zero(args = (sock,root_dir,file_name,method,http_version,))
                            new_thread.start()
                            threads.append(new_thread)
                            sock_list.remove(sock)
                        elif http_version == 1.1:
                            new_thread = http_one_one(args = (sock,root_dir,file_name,method,http_version,))
                            new_thread.start()
                            threads.append(new_thread)
                            sock_list.remove(sock)

        for t in threads:
            t.join()            
    except KeyboardInterrupt:
        print("Ctrl+Z pressed... Shutting Down server")    
    
    s.close()
