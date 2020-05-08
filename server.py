import cherrypy
import sys
import random
from math import inf
import copy
import ai

gameState = {
	"game": [
		[ [],  [],  [], [0], [1],  [],  [],  [],  []],
		[ [],  [],  [], [1], [0], [1], [0], [1],  []],
		[ [],  [], [1], [0], [1], [0], [1], [0], [1]],
		[ [],  [], [0], [1], [0], [1], [0], [1], [0]],
		[ [], [0], [1], [0],  [], [0], [1], [0],  []],
		[[0], [1], [0], [1], [0], [1], [0],  [],  []],
		[[1], [0], [1], [0], [1], [0], [1],  [],  []],
		[ [], [1], [0], [1], [0], [1],  [],  [],  []],
		[ [],  [],  [],  [], [1], [0],  [],  [],  []]
	],
	"moves": [
		{#exemple type :
			"move": {
				"from": [0, 3],
				"to": [1, 4]
			},
			"message": "I'm Smart"
		}],
	"players": ["LUR", "LRG"],
	"you": "LUR"
}

class Server:

	@cherrypy.expose
	@cherrypy.tools.json_in()
	@cherrypy.tools.json_out()
	def move(self):
		# Deal with CORS
		cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
		cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
		cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
		if cherrypy.request.method == "OPTIONS":
			return ''

		body = cherrypy.request.json
		print(body)
		### Do The thinking here ###
		gameState = []
		unchanged = []
		gameState = body["game"]
		
		print("I GOT SOMETHING")
		#Flip the player color if the AI is the second player, so the AI always gets the case that it plays as "color 0"

		
		print(gameState)
		if body["you"] == body["players"][1] :
			for y in range(len(gameState)) :
				for x in range(len(gameState[y])):
					for e in range(len(gameState[y][x])):
						gameState[y][x][e] = 1-gameState[y][x][e]



		unchanged = copy.deepcopy(gameState)
		#print(self.actions(gameState))
		print("############################")
		#print(self.actions(unchanged))
		#run the AI, which returns a path
		depth = 1
		if len(ai.actions(gameState)) > 40 :
			depth = 2
		else :
			depth = 5

		print(depth)
		path = ai.alphaBetaSearch(gameState, depth)
		print("AI ran")
		print(gameState)
		print(unchanged)
		#print(ai.actions(gameState))
		if not path :
			if ai.actions(unchanged) :
				path = ai.actions(unchanged)[0]
			else :
				print("TEAPOT ERROR")
				return {"move": {"from": [], "to": []}, "message": "Game seems to be over, or I'm a teapot, both are possible."}
		print(path)
		chosenItemOldX = path[0]
		chosenItemOldY = path[1]
		chosenItemNewX = path[2]
		chosenItemNewY = path[3]
		
		############################
		return {"move": {"from": [chosenItemOldY, chosenItemOldX], "to": [chosenItemNewY, chosenItemNewX]}}

	@cherrypy.expose
	def ping(self):
		return "pong"

	@cherrypy.expose
	def run(self, _myport):
		cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': _myport})
		cherrypy.quickstart(Server())
