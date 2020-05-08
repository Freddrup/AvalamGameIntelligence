import cherrypy
import sys
import random

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
		currentGrid = body["game"]
		itemsFound = {}
		itemNumber = 0
		print(currentGrid)
		print("############################")
		# Find all entities
		y=0
		for lines in currentGrid :
			x=0
			for columns in lines :
				if columns :
					itemsFound[str(itemNumber)] = [x, y, columns]
					itemNumber +=1
				x+=1
			y+=1
		print(itemsFound)
		itemNumber -= 1
		# Choose a random entity, and return move to make
		randomItem = []
		while not randomItem :
			randomItem = self.chooseRandom(itemNumber, itemsFound)
		
		chosenItemOldX = randomItem[0]
		chosenItemOldY = randomItem[1]
		chosenItemNewX = randomItem[2]
		chosenItemNewY = randomItem[3]
		print("############################")
		############################
		return {"move": {"from": [chosenItemOldY, chosenItemOldX], "to": [chosenItemNewY, chosenItemNewX]}}

	# function to find an entity with a height inferior to 5
	def chooseRandom(self, _itemNumber, _itemsFound) :
		_chosenItemHeight = 5
		_randomItem = 0
		_returnList = []
		while _chosenItemHeight is 5 :
			_randomItem = random.randint(0, _itemNumber)
			_chosenItemHeight = len(_itemsFound[str(_randomItem)][2])
		
		_chosenItemOldX = _itemsFound[str(_randomItem)][0]
		_chosenItemOldY = _itemsFound[str(_randomItem)][1]
		_surroundingItems = {}
		_surroundingItemNumber = 0
		for _items in _itemsFound :
			if _items == str(_randomItem) :
				print("found myself !")
			else :
				if _itemsFound[_items][2] :
					if _itemsFound[_items][0] == _chosenItemOldX or _itemsFound[_items][0] == _chosenItemOldX + 1 or _itemsFound[_items][0] == _chosenItemOldX - 1 :
						if _itemsFound[_items][1] == _chosenItemOldY or _itemsFound[_items][1] == _chosenItemOldY + 1 or _itemsFound[_items][1] == _chosenItemOldY - 1 :
							if ((len(_itemsFound[_items][2])+_chosenItemHeight) <= 5) :
								print("found acceptable neighbor item !")
								_surroundingItems[str(_surroundingItemNumber)] = _items
								_surroundingItemNumber += 1
		if len(_surroundingItems) == 0 :
			return []
		else :
			print("NEIGHBORS NEIGHBORS NEIGHBORS")
			print(_surroundingItems)
			_surroundingItemNumber -= 1
			_returnList.append(_chosenItemOldX)
			_returnList.append(_chosenItemOldY)
			_randomItemTowards = random.randint(0, _surroundingItemNumber)
			_chosenItemNewX = _itemsFound[_surroundingItems[str(_randomItemTowards)]][0]
			_chosenItemNewY = _itemsFound[_surroundingItems[str(_randomItemTowards)]][1]
			_returnList.append(_chosenItemNewX)
			_returnList.append(_chosenItemNewY)
			
			return _returnList


		return []


	@cherrypy.expose
	def ping(self):
		return "pong"

	@cherrypy.expose
	def run(self, _myport):
		cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': _myport})
		cherrypy.quickstart(Server())

if __name__ == "__main__":
	
	if len(sys.argv) > 1:
		myport=int(sys.argv[1])
	else:
		myport=4269
	

	cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': myport})
	cherrypy.quickstart(Server())

