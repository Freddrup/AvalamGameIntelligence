import socket
import json

playerDict = {
	"matricules": [""],
	"port": 0,
	"name": ""
}

def sendJSON(socket, data):
	msg = json.dumps(data).encode('utf8')
	total = 0
	while total < len(msg):
		sent = socket.send(msg[total:])
		total += sent



def subscribeToSupervisor(_name, _matricules, _supervisorHost, _myport, _subport):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((_supervisorHost, _subport))
	playerDict["name"] = _name
	playerDict["matricules"] = _matricules
	playerDict["port"] = _myport
	sendJSON(s, playerDict)
	print("subscription sent")
	# data = s.recv(1024)
	s.close()
	# print('Received', repr(data))

