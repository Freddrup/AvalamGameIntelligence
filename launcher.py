import sys
from subscribe import subscribeToSupervisor
from server import Server                    # Comment this line for random play behavior
#from serverRandom import Server             # Uncomment this line for random play behavior

myport = 8008                                # Variable that stores the port used by this player

if __name__ == "__main__":                   # See if there is a port argument, otherwise use port 8008
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
subscribeToSupervisor(name, matricules, supervisorHost, myport, subport)    # Subscribe to the game supervisor

s = Server()
s.run(myport)                               # Run the AI server