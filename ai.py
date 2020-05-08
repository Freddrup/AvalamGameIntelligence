###################################################################
#
# This code is a classic alpha-beta search algorithm 
# (same routines as MINIMAX), based on an example in chapter 5 of
# "Artificial Intelligence: A Modern Approach (3rd edit)" 
# - Stuart RUSSEL, Peter NORVIG, 2010.
#
###################################################################

from math import inf
import pickle

# Classic alpha-beta search algorithm (same routines as MINIMAX)
def alphaBetaSearch( gameState, depth) :
	answer = maxValue(gameState, -inf, inf, depth) # answer = [[fromX, fromY, toX, toY], utilityValue]
	return answer[0] #moveToMake

def maxValue(_gameState, alpha, beta, depth) :
	_localGameState = _gameState
	#print(depth)
	answer = [[], 0]
	if (gameIsOver(_localGameState) or depth <= 0):
		answer[1] = utility(_localGameState)
		return answer
	answer[1] = -inf
	for a in actions(_localGameState) :
		answer[1] = max(answer[1], minValue(result(_localGameState, a), alpha, beta, depth-1)[1])
		if answer[1] >= beta :
			#print("PRUNED BETA")
			#print(depth)
			answer[0] = a
			return answer
		alpha = max(alpha, answer[1])
	return answer

def minValue(_gameState, alpha, beta, depth) :
	#print(depth)
	_localGameState = _gameState
	answer = [[], 0]
	if (gameIsOver(_localGameState) or depth <= 0):
		answer[1] = utility(_localGameState)
		return answer
	answer[1] = inf
	for a in actions(_localGameState) :
		answer[1] = min(answer[1], maxValue(result(_localGameState, a), alpha, beta, depth-1)[1])
		if answer[1] <= alpha :
			#print("PRUNED ALPHA")
			#print(depth)
			answer[0] = a
			return answer
		beta = min(beta, answer[1])
	return answer

# HEURISTIC FUNCTION : return value dependent of the state of the game.
# This is the whole reason why this algorithm works, and could
# be greatly improved and optimised.
def utility(_gameState): 
	_localGameState = _gameState
	
	numberOfPiles = 0
	numberOfMyPiles = 0
	numberOfOtherPiles = 0
	numOf5HighPiles = 0
	numOf4HighPiles = 0
	for rows in _localGameState :
		for piles in rows :
			if len(piles) != 0 :
				if piles[len(piles)-1] == 1 :
					numberOfMyPiles += 1
					numberOfPiles += 1
					if len(piles) == 4 :
						numOf4HighPiles +=1
					if len(piles) == 5 :
						numOf4HighPiles +=1
				else :
					numberOfPiles += 1
					numberOfOtherPiles+=1
	try :
		_utility = (numberOfMyPiles-numberOfOtherPiles)*((numOf4HighPiles+numberOfPiles)/numberOfPiles)*((numOf4HighPiles+numberOfPiles)/numberOfPiles)*((numOf5HighPiles+numberOfPiles)/numberOfPiles)*(numberOfPiles/numberOfOtherPiles)
	except ZeroDivisionError :
		_utility = inf
	except :
		pass
	return _utility

# Returns a list of all possible moves, dependent on the current gamestate.
# Note : If some value names seem weird, it's because I used the code of
# ServerRandom.py, and didn't have the time to adapt the value names.
def actions(_gameState): 
	_localGameState = _gameState
	moves = []

	itemsFound = {}
	itemNumber = 0
	
	y=0
	for lines in _localGameState :
		x=0
		for columns in lines :
			if columns :
				itemsFound[str(itemNumber)] = [x, y, columns]
				itemNumber +=1
			x+=1
		y+=1
	#print(itemsFound)
	itemNumber -= 1

	_chosenItemHeight = 5
	_randomItem = 0
	
	for pilesFoundIndex in itemsFound :
		_randomItem = pilesFoundIndex
		_chosenItemHeight = len(itemsFound[pilesFoundIndex][2])
		if _chosenItemHeight >= 5 :
			pass
		else :
			_chosenItemOldX = itemsFound[_randomItem][0]
			_chosenItemOldY = itemsFound[_randomItem][1]
			_surroundingItems = {}
			_surroundingItemNumber = 0
			for _items in itemsFound :
				if _items == _randomItem :
					#print("found myself !")
					pass
				else :
					if itemsFound[_items][2] :
						if itemsFound[_items][0] == _chosenItemOldX or itemsFound[_items][0] == _chosenItemOldX + 1 or itemsFound[_items][0] == _chosenItemOldX - 1 :
							if itemsFound[_items][1] == _chosenItemOldY or itemsFound[_items][1] == _chosenItemOldY + 1 or itemsFound[_items][1] == _chosenItemOldY - 1 :
								if (len(itemsFound[_items][2])+_chosenItemHeight) <= 5 :
									#print("found acceptable neighbor item !")
									tempFoundPath = []
									tempFoundPath.append(_chosenItemOldX)
									tempFoundPath.append(_chosenItemOldY)
									tempFoundPath.append(itemsFound[_items][0])
									tempFoundPath.append(itemsFound[_items][1])
									moves.append(tempFoundPath)
		
	#print(moves)

	return moves # list of possible moves, with [fromX, fromY, toX, toY].

# Creates a new state list of the game after an action has taken place. 
def result(_gameState, action) :
	_localGameState = pickle.loads(pickle.dumps(_gameState))
	fromX = action[0]
	fromY = action[1]
	toX = action[2]
	toY = action[3]

	if _localGameState[toY][toX]:
		if len(_localGameState[toY][toX])+len(_localGameState[fromY][fromX]) <= 5 :
			_localGameState[toY][toX].extend(_localGameState[fromY][fromX])
			_localGameState[fromY][fromX] = []
	return _localGameState

# Returns true if no possible moves exists, otherwise returns false
def gameIsOver(_gameState) :
	_localGameState = _gameState
	if actions(_localGameState) :
		return False
	return True


