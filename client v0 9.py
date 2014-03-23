import timeit
import socket
import time
import resource
import select
import threading
import os

serv_port = 4090
ip_address = 'localhost'
thread_lock = threading.Lock()

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

class http_one_one(threading.Thread):
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
        self.count = 0
        self.running = 1
        self.start_time = ''
        self.stop_time = ''
        self.var1 = 1.0
        self.var2 = 1.1
        
    def run(self):
        start_timer = timeit.default_timer()
        self.socket_bind()
        self.connect_to_server()
        self.start_time = timeit.default_timer()
        self.running = 1
        while(self.running):
            self.send_request()
            if self.recv_data() == True:
                self.stop_time = timeit.default_timer()
                print ("The round trip time for this request is:", (self.stop_time-self.start_time),"seconds")
            else:
                timed_out = int(self.stop_time) - int(self.start_time)
                if timed_out > 15:
                    self.client_close()
            self.file_request = self.file_request + 1
        end_timer = timeit.default_timer()
        print("The time taken for the whole connection tear down is:", (end_timer-start_timer),"seconds")

    def socket_bind(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.bind((ip_address,client_port))

    def connect_to_server(self):
        try:
            self.client_socket.connect((self.server_ip_address,self.serv_port))
            print ("Client with port number", self.client_port,"Connected to the server")
        except OSError:
            print ("Client with port number", self.client_port,"is not able to connect to the server")

    def get_file_request(self):
        print (self.file_request)
        if self.file_request == 0:
            self.data = 'GET / HTTP/1.1'
        elif self.file_request == 1:
            self.data = 'GET / HTTP/1.1'
        elif self.file_request == 2:
            self.data = 'GET /reg.html HTTP/1.1'
    
    def send_request(self):
        self.get_file_request()
        try:
            print("hello")
            self.client_socket.send(bytes(self.data,'utf-8'))
        except BrokenPipeError:
            print ("Client with port number", self.client_port,"is not able to send any messages")
            
    def recv_data(self):
        try:
            buff = (self.client_socket.recv(1024)).decode(encoding = 'UTF-8')
            if buff:
                print("The data recieved for client with", self.client_port,"port number is:", buff)
                self.file_request = self.file_request + 1
                return True
            if buff.endswith('QUIT'):
                self.start_time = timeit.default_timer()
                return True
            else:
                return False
        except OSError:
            print ("Client with port number",self.client_port,"is not able to recieve messages")
            return False

    def send_quit_to_server(self):
        self.client_socket.send(bytes('QUIT','utf-8'))
        
    def client_close(self):
        print("The client with", self.client_port," port number is closing its connection")
        self.send_quit_to_server()
        self.client_socket.close()



if "__main__" == __name__:
    threads = []
    while(1):
        print ("1. Testing HTTP1.0 with three different connections")
        print ("2. Testing HTTP1.1 with three different connections")
        print ("3. Testing how many connections can the server handle")
        print ("4. Testing how much load can the server handle i.e total connections and requests")
        choice = int(input("Enter a choice:"))
        if choice == 1:
            cond = 1.0
            for cli_port in range(7290,7299):
                new_thread = http_one_zero(args = (cli_port, serv_port, ip_address, cond,))    
                new_thread.start()
                '''threads.append(new_thread)
                for t in threads:
                    if t.isAlive:'''            
                new_thread.join()
                for t in threads:
                    if t.isAlive():
                        print("Running", t)
        elif choice == 2:
            cond = 1.1
            for cli_port in range(15793, 15796):
                new_thread = http_one_one(args = (cli_port, serv_port, ip_address, cond,))
                new_thread.start()
                threads.append(new_thread)
            for t in threads:
                t.join()
