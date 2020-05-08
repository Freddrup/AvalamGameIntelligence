import sys
from subscribe import subscribeToSupervisor
from server import Server                    # Comment this line for random play behavior
#from serverRandom import Server             # Uncomment this line for random play behavior

myport = 1001

if __name__ == "__main__":
	if len(sys.argv) > 1:
		myport=int(sys.argv[1])
		print("Custom port :")
		print(myport)
	else:
		myport=8008

subport = 3001
name = "AvalamGameIntelligence, powered by Fred Corp."
matricules = ["18053"]
supervisorHost = "0.0.0.0"
subscribeToSupervisor(name, matricules, supervisorHost, myport, subport)

s = Server()
s.run(myport)