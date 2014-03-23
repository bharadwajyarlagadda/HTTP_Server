import timeit
import socket
import time
import resource
import select
import threading
import sys
import os

serv_port = int(sys.argv[1])
ip_address = 'localhost'
timer = 0
count = 0
thread_lock = threading.Lock()

class server_thread(threading.Thread):
    def __init__(self, args = ()):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.data = file_name
        self.http_version = http_version
        self.ip_address = ip_address
        self.serv_port = serv_port
        self.start_time = ''
        self.stop_time = ''
        self.var1 = 1.0
        self.var2 = 1.1
        self.median_time = ''
        
    def run(self):
        global timer
        global count
        if self.http_version == self.var2:
            self.start_time = time.clock()
            self.send_request()
            self.recv_data()
            self.stop_time = time.clock()
            print ("The round trip time for this request is:", (self.stop_time-self.start_time),"seconds")
            timer = self.stop_time - self.start_time
            count = count + 1
        else:
            thread_lock.acquire()
            self.client_socket.connect((self.ip_address,self.serv_port))
            self.start_time = time.clock()
            self.send_request()
            self.recv_data()
            self.stop_time = time.clock()
            print ("The round trip time for this request is:", (self.stop_time-self.start_time),"seconds")
            timer = self.stop_time - self.start_time
            count = count + 1
            thread_lock.release()
    
    def send_request(self):
        try:
            self.client_socket.send(bytes(self.data,'utf-8'))
        except:
            print ("This Client is not able to send any messages")
        
    def recv_data(self):
        try:
            buff = (self.client_socket.recv(1024)).decode(encoding = 'UTF-8')
            if buff:
                print("The data recieved is:", buff)
            if buff.endswith('QUIT'):
                print("The client port number is closing its connection")
                '''self.client_close()'''
        except OSError:
            print ("The client is not able to recieve messages")
            '''self.client_close()'''
        
    def client_close(self):
        self.client_socket.close()

class http_one_zero(threading.Thread):
    def __init__(self, args = ()):
        threading.Thread.__init__(self)
        self.client_port = cli_port
        self.serv_port = serv_port
        self.server_ip_address = ip_address
        self.condition = cond
        self.file_request = ''
        self.file_request = 0
        self.client_socket = ''
        self.data = ''
        self.running = 1
        self.start_time = ''
        self.stop_time = ''
        self.var1 = 1.0
        self.var2 = 1.1
        self.median_time = ''
        
    def run(self):
        start_timer = timeit.default_timer()
        for i in range(0,3):
            self.file_request = i
            self.socket_bind()
            self.connect_to_server()
            self.start_time = timeit.default_timer()
            self.send_request()
            self.running = 1
            while(self.running):
                self.recv_data()
                self.stop_time = timeit.default_timer()
                print ("The round trip time for this request is:", (self.stop_time-self.start_time),"seconds")
        end_timer = timeit.default_timer()
        print("The time taken for the whole connection tear down is:", (end_timer-start_timer),"seconds")


        
    def socket_bind(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.bind((ip_address,self.client_port))

    def connect_to_server(self):
        try:
            self.client_socket.connect((self.server_ip_address,self.serv_port))
            print ("Client with port number", self.client_port,"Connected to the server")
        except OSError:
            print ("Client with port number", self.client_port,"is not able to connect to the server")

    def get_file_request(self):
        print (self.file_request)
        if self.condition == self.var1:
            if self.file_request == 0:
                self.data = 'GET / HTTP/1.0'
            elif self.file_request == 1:
                self.data = 'GET / HTTP/1.0'
            elif self.file_request == 2:
                self.data = 'GET /reg.html HTTP/1.0'
        else:
            if self.file_request == 0:
                self.data = 'GET / HTTP/1.1'
            elif self.file_request == 1:
                self.data = 'GET / HTTP/1.1'
            elif self.file_request == 2:
                self.data = 'GET /reg.html HTTP/1.1'
    
    def send_request(self):
        self.get_file_request()
        try:
            self.client_socket.send(bytes(self.data,'utf-8'))
        except BrokenPipeError:
            print ("Client with port number", self.client_port,"is not able to send any messages")
        
    def recv_data(self):
        try:
            buff = (self.client_socket.recv(1024)).decode(encoding = 'UTF-8')
            if buff:
                print("The data recieved for client with", self.client_port,"port number is:", buff)
            if buff.endswith('QUIT'):
                print("The client with", self.client_port," port number is closing its connection")
                self.client_close()
        except OSError:
            print ("Client with port number",self.client_port,"is not able to recieve messages")
            self.client_close()
        
    def client_close(self):
        self.running = 0
        self.client_socket.close()

def get_root_directory():
    file = open("httpd.txt","r")
    lines = file.readlines()
    for line in lines:
        if line.startswith('THRESHOLD'):
            directory = line.split()
    file.close()
    threshold = directory[1]
    if not threshold:
        print ("There is no threshold value which you have mentioned in the httpd file")
        sys.exit()
    return threshold

if "__main__" == __name__:
    threads = []
    timed = get_root_directory()
    print("1. HTTP 1.1 load test")
    print("2. HTTP 1.0 load test - There are 1000 clients who get connected to the server and ask for three different files")
    choice = int(input("enter your choice"))
    if choice == 1:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client_socket.connect((ip_address,serv_port))
        while(1):
            try:
                if timer<int(timed):
                    file_name = 'GET / HTTP/1.1'
                    http_version = 1.1
                    new_thread = server_thread(args = (client_socket, file_name, http_version,))    
                    new_thread.start()
                    threads.append(new_thread)
                    print(timer)
                    print(count)
                else:
                    for t in threads:
                        if t.isAlive():
                            t.join()
            except NameError:
                sys.exit(0)
    elif choice == 2:
        cond = 1.0
        for cli_port in range(8290,9290):
            new_thread = http_one_zero(args = (cli_port, serv_port, ip_address, cond,))    
            new_thread.start()
            '''threads.append(new_thread)
            for t in threads:
                if t.isAlive:'''            
            new_thread.join()
            for t in threads:
                if t.isAlive():
                    print("Running", t)
        
