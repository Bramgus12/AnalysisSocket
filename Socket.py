import socket
import urllib.request
import json


def removebytemarks(bytestring):
    return bytestring[2:len(bytestring) - 1]


def createClient():
    studentnumber = input("StudentNumber: ")
    classname = input("ClassName: ")
    groupname = input("GroupName: ")
    clientid = input("ClientID (1 or 2): ")
    if int(clientid) == 1:
        ipothermachine = input("Ip of other machine: ")
        return client(studentnumber, classname, groupname, clientid, ipothermachine)
    else:
        ipthismachine = input("Ip of this machine: ")
        return client(studentnumber, classname, groupname, clientid, ipthismachine)


def program(client):
    global data
    while True:
        if int(client.clientid) == 1:
            if client.connection.receiveddata is None:
                client.connection.openconnection("145.24.222.103", 8001)
                client.senddata("")
                client.senddata(client.getjsonstring())
                client.updatedata()
                client.connection.closeconnection()
            else:
                client.subconnection.openconnection(client.ip, 6969)
                client.subconnection.senddata(client.getjsonstring())
                client.subconnection.closeconnection()
                break
        else:
            if client.subconnection.receiveddata is None:
                client.subconnection.sockethost(client.ip, 6969)
                client.subconnection.listen()
                if client.subconnection.receiveddata is not None:
                    data = removebytemarks(client.subconnection.receiveddata)
                client.updatedata(source=data)
            else:
                client.connection.openconnection("145.24.222.103", 8001)
                client.senddata("")
                client.senddata(client.getjsonstring())
                break
    return


class client:
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
        if source is None:
            _object = self.datatoobject(source=source, main=main)
        else:
            _object = self.datatoobject(source=source)
        self.secret = _object["secret"]
        self.status = _object["status"]

    def datatoobject(self, source=None, main=True):
        if source is None:
            if main:
                object = fromjson(self.connection.receiveddata)
            else:
                object = fromjson(self.connection.receiveddata)
        else:
            object = fromjson(source)
        return object

    def senddata(self, message, main=True):
        if (main):
            socket = self.connection
        else:
            socket = self.subconnection
        socket.senddata(message)
        socket.recievedata()
        socket.printdata()

    def getjsonstring(self):
        return "{\"studentnr\": \""+self.studentnumber+"\", \"classname\":\""+self.classname+"\", \"clientid\":"\
               +str(self.clientid)+", \"teamname\":\""+self.teamname+"\", \"ip\":\""+self.localip+\
               "\", \"secret\":\""+self.secret+"\", \"status\":\""+self.status+"\"}"


class connection:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiveddata = None

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

    def openconnection(self, ip, port):
        self.socket.connect((ip, port))

    def senddata(self, data):
        self.socket.sendall(bytes(data, encoding="utf-8"))

    def recievedata(self):
        totaldata = self.socket.recv(11000)
        self.receiveddata = totaldata

    def printdata(self):
        print(str(self.receiveddata)[2:len(self.receiveddata) - 1])

    def closeconnection(self):
        self.socket.close()

    def sockethost(self, ip, port):
        self.socket.bind((ip, port))


def fromjson(object):
    newobject = json.loads(object)
    return newobject


program(createClient())
quit(0)
