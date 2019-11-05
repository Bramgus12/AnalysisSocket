#############################################################
#                                                           #
#           Names: Bilal Azrioual, Bram Gussekloo           #
#                       Class: INF2D                        #
#                                                           #
#                                                           #
#############################################################
import socket
import urllib.request
import json


def removebytemarks(bytestring):
    # Remove the bytemarks, so that it is normal to read.
    return bytestring[2:len(bytestring) - 1]


def createClient():
    # Get all the info that is needed for sending it to the server 
    studentnumber = input("StudentNumber: ")
    classname = input("ClassName: ")
    groupname = input("GroupName: ")
    clientid = input("ClientID (1 or 2): ")
    if int(clientid) == 1:
        # The IP of the other machine
        ipothermachine = input("Ip of other machine: ")
        return client(studentnumber, classname, groupname, clientid, ipothermachine)
    else:
        # IP of your own machine because there isn't an easy way to retrieve it in code
        ipthismachine = input("Ip of this machine: ")
        return client(studentnumber, classname, groupname, clientid, ipthismachine)


def program(client):
    global data
    while True:
        if int(client.clientid) == 1:
            # Check if there is data in the variable
            if client.connection.receiveddata is None:
                # open connection to the server
                client.connection.openconnection("145.24.222.103", 8001)
                # Send some dummy data to test the connection
                client.senddata("")
                # Send the real data
                client.senddata(client.getjsonstring())
                # Update the new data in the object client
                client.updatedata()
                # Close the connection
                client.connection.closeconnection()
            else:
                # Open the connection to the other machine
                client.subconnection.openconnection(client.ip, 6969)
                # Send the data to the other machine
                client.subconnection.senddata(client.getjsonstring())
                # Close the connection
                client.subconnection.closeconnection()
                break
        else:
            # Check if there is data in the variable
            if client.subconnection.receiveddata is None:
                # Host a server for the data that has to be sent back to the server
                client.subconnection.sockethost(client.ip, 6969)
                # Listen for data
                client.subconnection.listen()
                if client.subconnection.receiveddata is not None:
                    data = removebytemarks(client.subconnection.receiveddata)
                client.updatedata(source=data)
            else:
                # Open a connection to the server
                client.connection.openconnection("145.24.222.103", 8001)
                # Send dummy data to the server to test the connection
                client.senddata("")
                # Send the real data to the server
                client.senddata(client.getjsonstring())
                break
    return


class client:
    # The client information
    def __init__(self, studentnumber, classname, teamname, clientid, ip="", secret="", status=""):
        self.connection = connection()
        self.subconnection = connection()
        external_ip = urllib.request.urlopen('https://v4.ident.me').read().decode('utf8')
        self.studentnumber = studentnumber
        self.classname = classname
        self.teamname = teamname
        self.clientid = clientid
        self.secret = secret
        self.status = status
        self.localip = external_ip
        self.ip = ip

    def updatedata(self, source=None, main=True):
        # Update the data in the client object. Add secret and status
        if source is None:
            _object = self.datatoobject(source=source, main=main)
        else:
            _object = self.datatoobject(source=source)
        self.secret = _object["secret"]
        self.status = _object["status"]

    def datatoobject(self, source=None, main=True):
        # Make the data into the object
        if source is None:
            if main:
                object = fromjson(self.connection.receiveddata)
            else:
                object = fromjson(self.connection.receiveddata)
        else:
            object = fromjson(source)
        return object

    def senddata(self, message, main=True):
        # Send data to the server and receive it
        if (main):
            socket = self.connection
        else:
            socket = self.subconnection
        socket.senddata(message)
        socket.recievedata()
        socket.printdata()

    def getjsonstring(self):
        # make the data into a jsonstring
        return "{\"studentnr\": \""+self.studentnumber+"\", \"classname\":\""+self.classname+"\", \"clientid\":"\
               +str(self.clientid)+", \"teamname\":\""+self.teamname+"\", \"ip\":\""+self.localip+\
               "\", \"secret\":\""+self.secret+"\", \"status\":\""+self.status+"\"}"


class connection:
    # initialize a connection object
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiveddata = None

    # Listen for data send by another client
    def listen(self):
        self.socket.listen()
        conn, addr = self.socket.accept()

        with conn:
            print("Connected by", addr)
            totaldata = ""
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                totaldata = totaldata + str(data)
        self.receiveddata = totaldata

    # Open the connection to a server
    def openconnection(self, ip, port):
        self.socket.connect((ip, port))

    # Send the data to the server
    def senddata(self, data):
        self.socket.sendall(bytes(data, encoding="utf-8"))

    # Receive the data from the server
    def recievedata(self):
        totaldata = self.socket.recv(11000)
        self.receiveddata = totaldata

    # Print the data to the client
    def printdata(self):
        print(str(self.receiveddata)[2:len(self.receiveddata) - 1])

    # Close the connection to the server
    def closeconnection(self):
        self.socket.close()

    # Host a server
    def sockethost(self, ip, port):
        self.socket.bind((ip, port))


# Make an object from the json.
def fromjson(object):
    newobject = json.loads(object)
    return newobject

# Run the program
program(createClient())
quit(0)
