import socket
import os

# in another terminal after running this type: curl 0.0.0.0:8000
#curl 127.0.0.0.1:8000 -H "Host: www.google.ca" match header to what the server is connecting to. Host header is the only way it would know is the one we are requesting
#allocate a new socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

#listen on port 8000
server.bind(('0.0.0.0', 8000))#means to listen on all addresses
server.listen(1)
while True:
      print("Waiting for connections...")
      client,address = server.accept()
      print("Connected")
      print (address)
      pid = os.fork()
      if (pid == 0):
            #client is going to be curl, web browser or something like that
            outgoing = socket.socket()
            outgoing.connect(("www.google.ca", 80))
            outgoing.setblocking(0)#prevent indefinite waiting
            client.setblocking(0)
            while True:
                  try:
                    part = client.recv(1024)
                  except socket.error, exception:
                         if exception.errno == 11:
                            part = None
                         else:
                            raise
                  if(part is not None and len(part) == 0):
                     exit(0)
                  if (part):
                     outgoing.sendall(part)
                     print("< " + str(part))
                  try:
                    part = outgoing.recv(1024)
                  except socket.error, exception:
                         if exception.errno == 11:
                            part = None
                         else:
                            raise
                  if(part is not None and len(part) == 0):
                         exit(0)
                  if (part):
                     client.sendall(part)
                     print("> " + str(part))
