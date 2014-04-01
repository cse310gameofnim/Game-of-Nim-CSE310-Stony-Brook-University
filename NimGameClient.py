# TCP Client Code
import sys, time
from socket import * 

argv = sys.argv                      
host = argv[1]
port = argv[2]

# Command line argument is a string, change the port into integer
port = int(port)  

s=socket(AF_INET, SOCK_STREAM)      # Creates a socket

#Connection loop
while 1:
    
    #Parsing input
    while 1:    
        input = raw_input("Your input: ");
        
        words = input.split() #parse    
        print words[0]
        
 
        #Determine what user wants to do...
        if words[0] == "remove":        
            #REMOVE ELEMENTNUM SETNUM
            formattedmsg = "REMOVE " + str(words[1]) + " " + str(words[2])
            s.send(formattedmsg)
            break
        elif words[0] == "help":
            print helpmsg
            contine
        elif words[0] == "exit":
            s.send("EXIT")
            break
        elif words[0] == "login":
            s.connect((host,port))          # Connect to server address
            msg = s.recv(1024)              # Probably a wait msg if you first one connecting          
            if msg == "WAIT":
                print "Waiting for other player"
                msg = s.recv(1024)
                
            print msg
            inputname = raw_input("Your input: ");
            s.send(inputname)
            break
        else:
            print "Try another command again...\n"
    #This is the msg that you get regarding the game           
    msg=s.recv(1024) 
          
    #Parse the response
    if not msg:
        break
    elif msg == "PLAYERLEFT":
        print "The other player left the game... wait now\n"
        msg = s.recv(1024)
    elif msg == "NEGATIVEERROR":
        print "You entered a number to make a set negative... try again\n"
        continue
    elif msg == "ZEROERROR":
        print "You can't remove from an empty set, try again\n"
        continue
    elif msg == "LOSE":
        print "You lost the game..."
        msg = s.recv(1024)
    elif msg == "WIN":
        print "You won the game!"
        msg = s.recv(1024)
        
    print msg
s.close()                            # Closes the socket 
# End of code
