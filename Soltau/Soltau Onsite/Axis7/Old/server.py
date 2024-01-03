from ast import While
from cmath import pi
import select
import sys
from telnetlib import DO
import time
import socket
import argparse
from io import BytesIO
import subprocess

#Maximum Packet size for UDP
maxUdpSize=8195

#parser = argparse.ArgumentParser()
#parser.add_argument('port', type=int)
#args = parser.parse_args()

host = "127.0.0.1"
port = 9095
data_received_0 = -1
data_received_1 = -1
data_received_2 = "none"

def server_program():

    #port = args.port
    # Set up a TCP/IP server
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to server address and port
    tcp_socket.bind((host, port))
    
    # Listen on port 81
    tcp_socket.listen(1)
    
    #this is how to call "DiaAxis7.exe". Start it when your socket server is ready to accept a connection 
    #Parameters are:
    # 1. unique ID of the Networking device which is connected to the servo drive (u can find out by using slaveinfo.exe)
    # 2. EtherCAT cycle Time in µs -> 8000 means, every 8 ms EtherCAT inputs/outputs are refreshed
    # 3. IP Adress for the tcp socket which communicates with python
    # 4. The port for the tcp socket
    # 5. Receive Timeout for Tcp Socket in ms
    ### subprocess.run(["..\DiaAxis7\Release\DiaAxis7.exe", "\\Device\\NPF_{055F21B9-EBEA-4AD0-BF23-9A87D778A3AC} 8000 127.0.0.1 9095 1000"])


    ###Remark: to find out the right network interface ID, use slaveinfo.exe (e.g. under SOEM-master\test\win32\slaveinfo\bin\Release\x86)
    # open a command prompt and execute it from there
    # first, execute it without any parameters, so it returns all availabe network devices and its ID
    # you will get something like this:
    #>> Available adapters
    #>> Description : Microsoft Corporation, Device to use for wpcap: \Device\NPF_{A0EE7DDE-ACA6-4BAD-8907-C568E6CB22DB}
    #>> ... (more adapters...)
    #
    # then execute slaveinfo.exe [some device id] -sdo which will give you information about connected ethercat slaves, e.g.
    #>> slaveinfo.exe \Device\NPF_{A0EE7DDE-ACA6-4BAD-8907-C568E6CB22DB} -sdo
    #
    # If you execute it with the right ID, you will see some information and it tells you, that there is at least one slave connected


    # subprocess.run(["..\DiaAxis7\Release\DiaAxis7.exe","\\Device\\NPF_{08944A45-5A55-47EF-8518-32A88DA099A1}","8000","127.0.0.1","9095","1000"])
    while True:
        # subprocess.run(["..\DiaAxis7\Release\DiaAxis7.exe","\\Device\\NPF_{08944A45-5A55-47EF-8518-32A88DA099A1}","8000","127.0.0.1","9095","1000"])
        print("Waiting for connection, start DiaAxis7.exe now!")
        connection, client = tcp_socket.accept()
    
        try:
            print("Connected to client IP: {}".format(client))
            
            counter = 0
           
            while True:

                while True:
                    data = bytes("", 'ascii')
                    while True:
                            current = connection.recv(1)
                            data = data + current
                            if(current == b'\x03'):
                                break; 

                    if(data==(b'\x02' + bytes("listen",'ascii') + b'\x03')):
                        print("Client is Ready to receive next Command.")
                        break
                
                #send Command... 
                message = bytes("",'ascii')
                if(counter == 0):
                    message = bytes("getSlaveCount()",'ascii')
                elif(counter==1):
                    message = bytes("getPos(1)",'ascii')
                elif(counter==2):
                    message = bytes("getError(1)",'ascii')
                elif(counter==3):
                    message = bytes("enable(1)",'ascii') #enable Slave with number 1 (turn on motor power)
                elif(counter==4):
                    message = bytes("home(1)",'ascii') #move Slave with number 1 in home position
                # elif(counter==5):
                #     message = bytes("jogPos(1)",'ascii')    #manual movement in positive direction, this one is "non blocking" you will instantly receive success 
                #                                             #axis will move until it receives jogNeg or jogStop!
                # elif(counter==6):                           
                #     message = bytes("jogNeg(1)",'ascii')    #same as jogPos, but negative direction
                # elif(counter==7):
                #     message = bytes("jogStop(1)",'ascii')   #Ends the "jog" Movement
                elif(counter==8):
                    message = bytes("movePosAbs(1, 3000000, 1000)",'ascii') # move Slave 1 to absolute Position 3meters with velocity 1m/s
                                                                            # it is not checked if the position makes sense, 
                                                                            # so for e.g. a 5m axis use values between 0 and 5000000 only
                                                                            # you can also use the default speed by sending only slavenumber and position
                                                                            # movePosAbs(1, 3000000)
                                                                            # and you can also send acceleration and deceleration as shown for movePosRel
                elif(counter==9):
                    message = bytes("movePosRel(1, -500000, 1000, 500, 400)",'ascii')   # move Slave 1 in negative direction by 0.5meters with velocity 1m/s
                                                                                        # acceleration 0.5m/(s^2) and deceleration 0.4
                                                                                        # same possibilites as for movePosAbs (2, 3 or 5 parameters...)
                elif(counter==10):
                    message = bytes("disable(1)",'ascii') #turn off Motor power
                elif(counter==11):
                    message = bytes("exit()",'ascii') #Close DiaAxis7.exe

                output = b'\x02' + message + b'\x03'

                connection.send(output)   

                if(counter==11):
                    break

                #Check if "startProcessing is received" (will be send when command was received successfully)
                data = bytes("", 'ascii')
                while True:
                        current = connection.recv(1)
                        data = data + current
                        if(current == b'\x03'):
                            break; 
                if(data==(b'\x02' + bytes("startProcessing",'ascii') + b'\x03')):
                    print("Command received...now wait for result")
                else:
                    print("something went wrong...the command was not received (wrong spelling is also simply ignored.....)")


                #process responses of some commands....
                if(counter<3):
                    data = bytes("", 'ascii')
                    while True:
                        current = connection.recv(1)
                        data = data + current
                        if(current == b'\x03'):
                            break;  
                
                    if(counter == 0):
                        #Process answer of "getSlaveCount()"" Command

                        print("Number of EtherCat Slaves: " + chr(data[12]))
                    elif(counter==1):
                        #Process answer of "getPos()" Command (can be used e.g. to double check the position of the axis)  
                        print("Position is: " + chr(data[5]))
                    elif(counter==2):
                        #Process "getError()"
                        print("Error can return Error(0) (no Error), Error(-1) (Error), Error(-2) (Warning)")
                               
                #no answer from enable(1), home(1), movePosAbs, etc...
                #you will only receive success or failed after it is finished...



                #Wait for Response - either "success" or "failed"
                data = bytes("", 'ascii')
                while True:
                        current = connection.recv(1)
                        data = data + current
                        if(current == b'\x03'):
                            break;   
                if(data==(b'\x02' + bytes("success",'ascii') + b'\x03')):
                    print("Executing the command is finished, everything is ok!")
                else:
                    print("Executing the command failed...somethings wrong...")

                time.sleep(5) #wait a moment
                counter = counter + 1


    
        finally:
            connection.close()


if __name__ == '__main__':
    server_program()