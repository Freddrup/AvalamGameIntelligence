######################################################
#
# This code handles all the requests from the game 
# supervisor, defines what player it is playing (0 or
# 1), decides at which depth the AI needs to stop 
# searching, and requests the AI to find the best 
# possible move.
#
######################################################

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
	"moves": [],
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
		### It get's a bit interesting at this point ###
		gameState = []
		gameState = body["game"]
		unchanged = copy.deepcopy(gameState)
		print("I GOT SOMETHING")
		
		#Flip the player color if the AI is the second player, so the AI always gets the case that it plays as "color 0"
		print(gameState)
		if body["you"] == body["players"][1] :
			for y in range(len(gameState)) :
				for x in range(len(gameState[y])):
					for e in range(len(gameState[y][x])):
						gameState[y][x][e] = 1-gameState[y][x][e]

		print("############################")
		# Decide at which depth the AI needs to stop digging
		depth = 1
		if len(ai.actions(gameState)) > 40 :
			depth = 2
		else :
			depth = 5

		print(depth)
		# Run the AI, which returns a path
		path = ai.alphaBetaSearch(gameState, depth)
		print("AI ran")
		print(gameState)
		print(unchanged)

		# Handle teapot errors (error if the server gives a game state 
		# with no possible moves, or the ai.actions(gameState) function
		# is broken). this aways gives a bad move.
		if not path :
			if ai.actions(unchanged) :
				path = ai.actions(unchanged)[0]
			else :
				print("TEAPOT ERROR")
				return {"move": {"from": [0,0], "to": [0,0]}, "message": "Game seems to be over, or I'm a teapot, both are possible."}
		print(path)
		chosenItemOldX = path[0]
		chosenItemOldY = path[1]
		chosenItemNewX = path[2]
		chosenItemNewY = path[3]
		
		# Send chosen move to game supervisor
		return {"move": {"from": [chosenItemOldY, chosenItemOldX], "to": [chosenItemNewY, chosenItemNewX]}}

	@cherrypy.expose
	def ping(self):
		return "pong"

	@cherrypy.expose
	def run(self, _myport):
		cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': _myport})
		cherrypy.quickstart(Server())
