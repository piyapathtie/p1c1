#!/usr/bin/env python

from urlparse import urlparse
import socket as skt
import os
import sys
import asyncore

severName = sys.argv[-1]
fileName = sys.argv[-2]
severPort = 8080

host = urlparse(severName).hostname
path = urlparse(severName).path


def get(host, path):
    return ("GET {n} HTTP/1.1\r\n" + "Host: {s}\r\n\r\n").format(s=host, n=path)


print "start"
clientSocket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
clientSocket.connect((host, severPort))
print "connnect...."
request_str = get(host,path)
clientSocket.send(request_str)

receive = 0
header = ""
with open (fileName, 'wb') as f:
    while True:
        datareceive = clientSocket.recv(8192)
        header += datareceive 
        if "\r\n\r\n" in header:
            headerFinal, remain = header.split("\r\n\r\n")
            receive += len(remain)
            f.write(remain)
            break
             
    contentLen = headerFinal[headerFinal.find("Content-Length")+16 : header.find("Connection")-1]
    print contentLen
             
    while receive != contentLen:
        datareceive = clientSocket.recv(8192)
        receive += len(datareceive)
        f.write(datareceive)
        print receive

        # if len(receive) == contentLen:
        #     clientSocket.close()
        #     break 

    clientSocket.close()
    f.close()
    
# print headerFinal
# print len(receive)
# print len(receive) 


# print contentLen

# for each in receive:
#     header += each
#     if "\r\n\r\n" in header:
#         break

# l = len(header)

# content = receive[l:]

# # print len(content)

# with open('/home/dc/Downloads/tie', 'wb') as f:
#     print 'file open'
#     f.write(content)
# # clientSocket.close()
    
print "finish"