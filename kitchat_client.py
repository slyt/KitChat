# KitChat client

import socket
import sys
import select
import time

try: 
    import pygame
except ImportError:
    print "\n\n-------------------------------------------------------------------"
    print 'For sounds, please install pygame with "sudo apt-get install python-pygame"'
    print "if you\'re Kit and love Macs, here\'s the link..."
    print 'http://pygame.org/wiki/macintosh'
    print "-------------------------------------------------------------------\n\n"
#import pyaudio
#import wave

"""
try:
    import pyglet
except ImportError:
    print "failed to import pyglet module to play .wav sound file"
    print 'please install pyglet with "sudo apt-get install python-pyglet"'
"""


pygame.init()
print 'Welcome to KitChat, the world\'s best chat client'

#get username that will be prepended to data sent
username = str(raw_input('What is your username? >> '))
if (username == ""):
    print "No username inputted: logging in as Anonymous"
    username = "Anonymous"
else:
    print 'Logging in as "' + username + '"'


def prompt():
    sys.stdout.write('>>')
    sys.stdout.flush()

def playSendSound():
    pygame.mixer.music.load('./sounds/mesg_sent.wav')
    pygame.mixer.music.play() 
    #song = pyglet.media.load('./sounds/mesg_sent.wav')
    #song.play()
    #pyglet.app.run()

def playRecvSound():
    pygame.mixer.music.load('./sounds/mesg_recv.wav')
    pygame.mixer.music.play() 
    #song = pyglet.media.load('./sounds/mesg_recv.wav')
    #song.play()
    #pyglet.app.run()

def playLoginSound():
    pygame.mixer.music.load('./sounds/buddyin.wav')
    pygame.mixer.music.play() 

def playLogoffSound():
    pygame.mixer.music.load('./sounds/buddyout.wav')
    pygame.mixer.music.play() 

"""
def playSound(wavFile):
    #define stream chunk   
    chunk = 1024  

    #open a wav format music  
    f = wavFile 
    #instantiate PyAudio  
    p = pyaudio.PyAudio()  
    #open stream  
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)  
    #read data  
    data = f.readframes(chunk)  

    #paly stream  
    while data != '':  
        stream.write(data)  
        data = f.readframes(chunk)  

    #stop stream  
    stream.stop_stream()  
    stream.close()  

    #close PyAudio  
    p.terminate()
"""

if __name__ == "__main__":

    
    # default server parameters
    hostname = "localhost"
    port = 5999
    RECV_BUFFER=4096

    # resolve default hostname
    try:
        hostIP = socket.gethostbyname (hostname)
    except socket.gaierror:
        print "Hostname could not be resolved. Exiting..."
        sys.exit(-1)
    

    # parse command line arguments
    if (len(sys.argv) == 2): # IP specified, but no Port
        hostname = sys.argv[1] #
        print "argv == 2, hostname==" + str(hostname)
        try: 
            hostIP = socket.gethostbyname(hostname)
            print "Connecting to KitChat server at " + str(hostIP) + " using default port " + str(port)
        except socket.gaierror:
            print "Hostname could not be resolved."
            print "KitChat usage: python kitchat.py <hostname> <port>"
            print "Exiting..."
            sys.exit(-1)
            
    elif ( len(sys.argv) == 3): # IP and port specified
        hostname = sys.argv[1]
        port = int(sys.argv[2])
        try: 
            hostIP = socket.gethostbyname(hostname)
            print "Connecting to KitChat server at " + str(hostIP) + " using port " + str(port)
        except socket.gaierror:
            print "Hostname could not be resolved."
            print "KitChat usage: python kitchat.py <hostname> <port>"
            print "Exiting..."
            sys.exit(-1)
    else: #use defaults
        print "No hostname specified. Connecting to KitChat server at default IP address " + str(hostIP) + " on default port " + str(port)
    

    # create socket descriptor: IPv4 using TCP
    try: 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print'socket creation failed.' + str(msg[0]) + msg[1]
        sys.exit(-1)


    # connect to remote host
    try:
        s.connect((hostIP,port))
        print "Socket CONNECTED to " + hostname + " on port " + str(port)
    except:
        print "Unable to connect to " + str(hostIP) + " on port " + str(port)
        sys.exit(-1) 


    
    # open wav audio files
    #sndSend = wave.open(r"./sounds/mesg_sent.wav","rb")
    #sndRecv = wave.open(r"./sounds/mesg_recv.wav","rb")
    

    prompt()
    playLoginSound()

    #send name to server as first message
    s.send(username)

    while 1:
        socket_list = [sys.stdin, s] # pipes/sockets to monitor
        
        # block with select() until a user inputs data to stdin or the server responds on socket s
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
        
        for sock in read_sockets:
            # mesg for you sir
            if sock == s:
                data = sock.recv(RECV_BUFFER)
                if data:
                    sys.stdout.write(data)
                    #playSound(sndRecv)
                    playRecvSound() # play AIM receive sound
                    #print "\nRECEIVE DATA!"
                    prompt()
                else:
                    print "\nDisconnected from KitChat server " + str(hostIP)
                    sys.exit()
                        
            else: #user sent something to stdin
                msg = sys.stdin.readline() # prepend username so it get's sent to the server
                s.send(msg)
                print "[SENT DATA]"
                playSendSound()
                #playSound(sndSend) # play AIM send sound
                prompt()

    time.sleep(10)
    print "done sleeping, disconnecting"
    s.shutdown(1)
    s.close()






