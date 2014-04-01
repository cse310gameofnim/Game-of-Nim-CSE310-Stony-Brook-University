#Kalon Cheong
#107712864
#Nim Game Server
 
from socket import *
import thread, random

def swap(num):
    if(num == 0):
        return 1
    else:
        return 0

def setUpSetArray():
    #Init the game data
    numberOfSets = random.randint(3,5) #Number of sets, 3 to 5
    setArray=[]
    for num in range(1,numberOfSets):
        setArray.append(random.randint(1,7)) #Elements per set, 1 to 7
    return setArray    
    
def allZero(array):
    #Return True if the array is all zeroes
    for num in array:
        if num != 0:
            return False
    return True
            
if __name__ == "__main__":
    host="127.0.0.1"
    port=7864
    
    s=socket(AF_INET, SOCK_STREAM)
    s.bind((host,port))                 # Binds the socket. Note that the input to 
                                                # the bind function is a tuple
     
    s.listen(2)                         # Sets socket to listening state with a  queue
                                                # of 1 connection
    print "Listening for connections.. "

    #Active connection flags...
    BStillCon = False;
    AStillCon = False;
    
    while 1:
        
        #Wait for two players...
        if AStillCon is False:
            (clientsocketA,clientaddrA)=s.accept()
            clientsocketA.send("WAIT")
            print "First addr is ", clientaddrA
        
        if BStillCon is False: 
            (clientsocketB,clientaddrB)=s.accept() 
            print "Second addr is ", clientaddrB
        
        AStillCon = False
        BStillCon = False
        
        #thread.start_new_thread(handler, (clientsocketA, clientaddrA, clientsocketB, clientaddrB));
        
        #Ask users for their name        
        clientsocketA.send("Enter your name:")
        clientsocketB.send("Enter your name:")
                
        #Get that name response...
        nameA = clientsocketA.recv(1024)
        nameB = clientsocketB.recv(1024)
        
        print "First name was " + nameA
        print "Second name was " + nameB
        
        #Now enter the main loop...
        
        #Init the currentplayer
        currentplayer = 0
        currentsocket = clientsocketA
        othersocket = clientsocketB
        
        #Init the game data
        setArray = setUpSetArray()
        
        while 1:
            #Set up game data string to pass
            gamedata = ""
            
            for setnum in range(0, len(setArray)):
                gamedata += str(setnum) + " "
            
            gamedata += "\n"
            
            for num in setArray:
                gamedata += str(num) + " "
            
            gamedata += "\n"
            
            #Multiplexing the current player, 0 = A, 1 = B
            if currentplayer == 0:
                currentsocket = clientsocketA
                othersocket = clientsocketB
            else:
                currentsocket = clientsocketB
                othersocket = clientsocketA
            
            #Send data
            print gamedata
            currentsocket.send(gamedata)
            
            #Get command
            data = currentsocket.recv(1024);
            words = data.split()
            command = words[0]
            print command

            if command == "EXIT":
                #Kill both sockets
                currentsocket.close()
                othersocket.send("PLAYERLEFT")
                
                if othersocket == clientsocketA:
                    AStillCon = True
                else:
                    BStillCon = True
                
                break
            elif command == "REMOVE":
                snToRemoveFrom = int(words[2])
                elementsToRemove = int(words[1])
                
                if(setArray[snToRemoveFrom] - elementsToRemove < 0):
                    #Error...
                    currentsocket.send("NEGATIVEERROR")
                elif(setArray[snToRemoveFrom] == 0 or elementsToRemove == 0):
                    currentsocket.send("ZEROERROR")
                else:
                    setArray[snToRemoveFrom] -= elementsToRemove
                    currentplayer = swap(currentplayer)
                    if allZero(setArray):
                        currentsocket.send("WIN")
                        othersocket.send("LOSE")
                        setArray = setUpSetArray() #Winner plays first
                        continue
                    
            else:
                currentplayer = swap(currentplayer)
                
        break      
        
    s.close()
