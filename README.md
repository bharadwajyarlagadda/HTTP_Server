HTTP_Server
===========

Server which uses socket functionality for implementing HTTP 1.0 and HTTP 1.1 requests

About Server:

Our server does the following activities:

 It creates a socket
 It binds to the ‘localhost’ specified inside the program and the port given in the argument
 It goes into listen state (listens forever)
 When any client requests connection, it first accepts the connection and then goes into the receiving mode.
 We have implemented this by using select() function.
 When any client sends in any request it first parses the entire url and then checks for whether the request is HTTP 1.0 or HTTP 1.1
 Based on whether it is HTTP 1.0 or HTTP 1.1, the further functionality will depend.


How we have implemented HTTP 1.0 functionality?

The main functionality which we have implemented is as follows:

 Whenever any client asks for a file, the server immediately launches a thread for that particular client and processes that request and sends the needed file’s data to the client. In our case we just have taken a small file (index.html) which can be less than or equal to 1024 Bytes.
 When the server completes the whole thread it closes of the connection to the client.
 If the same client needs another file it has to open up a new connection and has to connect to the server and go through the same process mentioned above.
 In this case whatever connections are made will be disconnected immediately after the server processing is done.
 The implementation we have done in the server end is whatever might be the number of threads will be created at a moment for number of clients; parallel execution of all the threads happen and finally they join up in the main thread once their functionality is done.



How we have implemented HTTP 1.1 functionality? The main functionality is as follows:

 There will be only one client and one server in this case. 
 First of all, they get connected.
 Once they have connected the client goes on asking number of requests (in our case we have asked the same file number of times – it is a never ending loop (while(1))).
 The client goes inside a loop and goes on asking number of requests.
 The server then allocates each request a thread and makes it running (processing).
 We have chosen this functionality because of the following reason:

o To see how many requests can a server handle once the connection is established in a threshold value. (we can see how many requests that a server can handle on a connection)
o The connection made between server and client will be broken once it reaches a threshold value. 
o We have taken several threshold values based on the system’s performance, which we will discuss in the further section.
o We check the threshold value on the client side. 
o We have taken the threshold value on the client side because of the concept of persistent connection.

 Persistent Connection: A persistent connection is something which helps the client connected to a server in a given amount of timeout. After the timeout , the server gets disconnected from the client
 Usually the timeout period will be on the server side, but for example if we take any browser like Mozilla or chrome(client) all the client browsers have a functionality of refreshing themselves after a certain period of time due to which the server gets to know that the client browser is still connected to it.
 In real world, a persistent connection involves both the server and the client browser having a timeout.
 For example, apache server has a timeout of 15 secs and Mozilla browser has a timeout of 60 secs.
 In our case this is a simple socket based communication in which each of them communicates on a period of time.
 As we are giving number of requests from the client we have put a threshold value on the client side.
 The threshold value is the amount of time the thread runs. If the time of a thread exceeds the threshold value, it immediately breaks of the loop.
 In this persistent connection, we have taken a thread for each request. So for each request, a thread will be initiated.
 We haven’t joined back the thread back into the main thread once its execution gets completed.
 We have made those threads stay like that.
 Whenever number of threads are alive the execution time of the further incoming threads become high because CPU checks all the threads that are alive in a process and process the appropriate thread which needs attention.
 We have inserted a global value for timer such that once the value of that global value increases than threshold; it helps to break down the connection.
 The execution also can depend on the number of threads which a system can generate. The number of threads mainly depends on the system specifications.
 We also have discussed about the system used for execution in further section.



System specifications:

 Operating system – CentOS 6 (virtual operating system)
 Number of processors – 2 (2 cores per processor – total 4 processor cores)
 RAM – 2 GB
 Hard Disk – 20 GB



Some more Details:

 We have changed the limits of the several variables inside the command prompt inorder to avail more number of threads in a given threshold.
 Some of the variable which we have changed are STACK_SIZE (main not the thread’s), NO_FILES (number of open file descriptors), NO_USR (number of user processes). These all variables can be changed only once per a command prompt window (i.e the values remain active until the command prompt is closed. Once the command prompt is closed, the values come back to their original values)
 The changing of the variables helped us in creating more number of threads. We can check the same by changing the system values.
 We have tested all the test cases on the same system which is mentioned above.



Results:

For Browser:

We have just implemented simple example for index.html which contains the text “hello world” in html content and it is working fine.

For HTTP 1.0:

Test cases:

The following readings are taken more than once (with 95% statistically correct with 1 or 2 % failures)

1) Calculate with 100 different clients (Tested twice)

The round trip time for every request is 0.002 sec. (This is an assumed average based on all the values)

The connection tear down for every connection is 0.011 to 0.015 sec. (This is assumed average range based on all output values)

2) Calculate with 300 different clients (Tested twice)

The round trip time for every request is 0.0014 to 0.0022 sec. (This is an assumed average based on all the values)

The connection tear down for every connection is 0.006 to 0.009 sec. (This is assumed average range based on all output values)

3) Calculate with 1000 different clients (Tested twice)

The round trip time for every request is 0.0016 to 0.0024 sec. (This is an assumed average based on all the values)

The connection tear down for every connection is 0.007 to 0.011 sec. (This is assumed average range based on all output values)

For HTTP 1.1:

1) Threshold = 4secs (testes twice)

No. requests handled by the server = 564

The round trip time for the requests varied from 0 to 4 sec with an assumed average of 2.7

2nd time tested

No. requests handled by the server = 578

The round trip time for the requests varied from 0 to 4 sec with an assumed average of 2.8 3rd time tested

No. requests handled by the server = 711

The round trip time for the requests varied from 0 to 4 sec with an assumed average of 2.8


I have taken the above threshold based on the system specifications and also the fact that no connection is to handle those many requests. It can be 5 in a row or 9 in a row but at a time there cant be abundant number of inputs from the same client.
The number of requests varies as both the server and client are running their separate threads. If client has 700 threads, the server might also be running the same amount of threads. And because of the memory sometimes threads stop by throwing an exception.
So, every time you execute for HTTP 1.1 it’s better you exit both server and client and then execute them again. The execution time varied as the threads become more and more and every time you need to close the terminal and open again
