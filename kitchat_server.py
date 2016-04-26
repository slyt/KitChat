# Broadcast message server

import socket
import select
import sys

print 'Hello World! I am the KitChat server. Your wish is my command!'

PORT = 5999

# CONNECTION_LIST will hold available clients
# We can read iterate through the list and see if there is data available on each socket
# if there is data, we want to relay it to the other clients (and ignore the one who sent it)


# send message from the input socket to the list of connected sockets, sans server socket.
def mesgAll (sock, message, name):
    if name==True: # prepend username to broadcast
        message = '\r' + ID[sock] + ": " + message + '\r'# prepend username 

    for socket in CONNECTION_LIST: # iterate through all connected clients
        if socket != serverSock and socket != sock: #disregard server and sender
            try:
                socket.send(message)
            except:
                socket.close() # failed
                CONNECTION_LIST.remove(socket) # bye bye client

if __name__ == "__main__":

    CONNECTION_LIST = [] # list of currently connected clients
    ID = {}
    RECV_BUFFER = 4096 # how much data we grab on each call to recv; recv talks to OS which buffers data on a lower level 
    
    if (len(sys.argv) == 2): # Port is first argument if provided
        PORT = int(sys.argv[1]) 
        
    # this is the socket used to accept connections by the server
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Socket options here:
    # default:  dissallow the socket/ip_address combo to be used until after a delay time (TIME_WAIT) has passed
    #           (to make sure all en route packets are dead)
    # SO_REUSEADDR: allows a new client to bind to a recently closed prot/IP combo instantly
    # socket.SO_SOCKET defines the level of the stack that we're working at - SOCKET level
    serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 3rd argument is to set it True or False
    
    # 0.0.0.0 will serve all network adaptors
    # 127.0.0.1 will only server clients on the same machine (i.g. if running serve/client(s) on colossus
    serverSock.bind(("0.0.0.0", PORT))
    serverSock.listen(20) # backlog is the pending connection buffer size, can be determined emperically under load

    CONNECTION_LIST.append(serverSock) 
    
     
    print "KitChat server started! (Port: " + str(PORT) + ")"
    
    while 1: #infinately handle clients! 
        # Using select because polling is goofy and interrupts (signals?) are the best
        # sending select the CONNECTION_LIST with the serverSock in it will allow the OS
        # to monitor the serverSock for clients wishing to connect
        #
        # 
        # Use select to wait/block until something exciting happens on a socket
        # in the CONNECTION_LIST
        read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST,[],[])
        
        for sock in read_sockets:
            if sock == serverSock: # if the excitement is happening on the server socket, we've got a new client!
                sockfd, addr = serverSock.accept() # accept the connection on the server socket, and push to unique socket
                CONNECTION_LIST.append(sockfd) # add the client to the currently connected list so we can monitor with select
                print  addr, "has connected"
                
                # clients send username as soon as they connect
                ID[sockfd] = sockfd.recv(RECV_BUFFER) # grab the name sent by the client
                print ID[sockfd] + " has joined the chat!"
                
                #print "connection list below: "
                #print CONNECTION_LIST    
                # users on the server side.
                # mesgAll(sockfd, "\nWelcome %s, %s to KitChat!\n" % addr)
                mesgAll(sockfd, "\n---%s has logged in---\n" % ID[sockfd], False)
            else: # we're getting information from a client socket
                data = sock.recv(RECV_BUFFER) # since using TCP stream, grab the buffer length
                if data: # do while(data): here in order to get more than just RECV_BUFFER size 
                    mesgAll(sock, data, True) # True means force client to prepend username before data is sent
                else: # connection died
                    mesgAll( sock, "\n---%s has logged off---\n" % ID[sock], False)
                    print ID[sock] + " (%s,%s) has logged off." % addr
                    #TODO Play AOL log-off sound, send special character codes
                    sock.close()
                    del ID[sock] # remove them from the dictionary
                    CONNECTION_LIST.remove(sock)
                    continue
                        
                #except: # the change the select() noticed was actually a socket disconnecting
                    #mesgAll( sock, "Client %s, %s has logged off." % addr)
                    #TODO Play AOL log-off sound
                    #CONNECTION_LIST.remove(sock)
                    #sock.close()
                    #continue

    server_socket.close() #if somehow we exit the while loop, relent the socket
