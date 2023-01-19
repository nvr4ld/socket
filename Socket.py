from socket import *

serverReply = ''
clientSocket = socket(AF_INET, SOCK_STREAM)                 #initializing socket with TCP

serverName = input("IP Address is: ")                       #input IP
serverPort = int(input("Port number is: "))                 #input port number

try:
    clientSocket.connect((serverName, serverPort))              #connecting to the server
    connection = True                                           #connection is established
    print("Successful connection, please type the command")

except:
    print("Failed to connect to the server")
    exit(0)

while(connection):                       
    clientInput = input("client: ")                         #get input and send it to the server
    clientSocket.send(clientInput.encode())
 
    if clientInput == "POST":                               #if the command is post
        post = True        

        while(post):                                        #keep receiving and sending inputs
            clientInput = input("client: ")

            try:                                                                       #try to send the input
                clientSocket.send(clientInput.encode())     
                print(f"\nIP Address: {serverName}\tPort Number: {serverPort}")        #print status
                print("Connect Status: OK\tSend Status: OK\n")

            except:                                                                    #if input wasn't sent
                print(f"\nIP Address: {serverName}\tPort Number: {serverPort}")        
                print("Connect Status: ERROR\tSend Status: ERROR\n")                   #status = error
                print("Reconnecting...")

                try:                                                   #try to connect again
                    clientSocket = socket(AF_INET, SOCK_STREAM)               
                    clientSocket.connect((serverName, serverPort))
                    print("Reconnected to the server, please type the command")
                    break                                              #break the loop of post     

                except:
                    print("Failed to reconnect to the server")           #if can't connect, print error 
                    clientSocket.close()                               #close the socket and exit the program
                    exit(0)

            if clientInput == '#':                          #until the input is #
                post = False
                serverReply = clientSocket.recv(2048)       #then receive the reply(OK) and print it
                print(serverReply.decode("utf-8"))

    elif clientInput == "QUIT":                             #if the command is quit
        serverReply = clientSocket.recv(2048)               #receive the reply of server and print it
        print(serverReply.decode("utf-8"))

        if serverReply.decode("utf-8") == "server: OK":     #if it is OK
            connection = False                              #close the connection

    elif clientInput == "READ":                             #if command is READ
        read = True

        while(read):                                        #keep receiving messages until the line contains only #
            
            try:                                            #try to receive message
                serverReply = clientSocket.recv(2048)
                print(f"\nIP Address: {serverName}\tPort Number: {serverPort}")
                print("Connect Status: OK\tRead Status: OK\n")                 #status is OK

            except:                                         #if message from server was anticipated, but wasn't received
                print(f"\nIP Address: {serverName}\tPort Number: {serverPort}")        
                print("Connect Status: ERROR\tSend Status: ERROR\n")           #status = Error
                print("Reconnecting...")

                try:                                                            #try to connect
                    clientSocket = socket(AF_INET, SOCK_STREAM)               
                    clientSocket.connect((serverName, serverPort))
                    print("Reconnected to the server, please type the command")
                    break                                                       #start from the beginning

                except:                                                         #if can't connect
                    print("Failed to reconnect to the server")                    #print Error
                    clientSocket.close()                                        #close socket and exit the program
                    exit(0)

            print(serverReply.decode("utf-8"))
            if(serverReply.decode("utf-8") == "server: #"):
                read = False

    else:                                                   #if command is invalid
        serverReply = clientSocket.recv(2048)               #receive the reply and print it
        print(serverReply.decode("utf-8"))
 
else:
    clientSocket.close()                                    #when QUIT is called, close the socket
    exit(0)                                                 #and terminate the program