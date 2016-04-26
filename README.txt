--------------------------------------------------------------
--------------------------------------------------------------
Welcome to KitChat the world's best chat program!


SERVER: to setup execute (port is optional):
python kitchat_server.py <port>


CLIENT: to connect simply execute:
python kitchat_client.py <hostname> <port>

default hostname = 0.0.0.0
default port = 5999


NOTE:   Be sure to install the pygame module so that the
        sounds work correctly. The sounds are client side
        and are located in ./sounds/ directory. So be sure
        to execute the client script in the parent directory
        of ./sounds/

FEATURES:
--Level 1--
- Server and client with programable ports
- Confirm sending message

--Level 2--
- Custom usernames (server keeps track, can login as Anonymous with no input)
- Broadcast message to everyone (except sender and server)
- Login/Logoff status updates on server (IP address, port, username)
- Login/Logoff status updates on clients (username only for security)

--Level buffet!--
- AOL Instant Messanger messaging sound effects!!! (oh the nastolgia)


Acknowledgments:

https://docs.python.org/3/library/socket.html
^ Good documentation for socket programming in python with simple examples

http://www.binarytides.com/code-chat-application-server-client-sockets-python/
^ My server is based on this. I made sure to understand each everthing, line-by-line
and provide appropriate comments. I even found a few bugs that people were asking
about in the comments and was able to debug and provide a fix for my code.
Essentially the same as C socket programming server/client assignment from CS3411 with Onder.
Modifications to keep track of usernames.

https://www.youtube.com/watch?v=hxVQ9rhjyTY
^ And of course, the nostalgic AIM sounds

--------------------------------------------------------------
--------------------------------------------------------------
