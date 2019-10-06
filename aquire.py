import matplotlib.pyplot as plt
import random
import time
import drawnow


#### Logic and datastructures to maintain game state ####


## Data Structure for hotel chain
class Chain:
	def __init__(self, uid):
		# uid is the chain identifier (1-6). Should never be 0
		self.uid = uid

		# UID of chain determines its luxury value
		if uid <= 2:
			self.lux_level = "low"
		elif uid <=4:
			self.lux_level = "med"
		else:
			self.lux_level = "high"

		# List of (x,y) tuples for chain territory
		self.territory = []

	## Return the value of the chain, were it to be liquidated.
	# If chain_size > 0, return the hypothetical price of that chain_size
	# If chain_size==-1, use current size of chain data structure for pricing
	# Todo, verify this logic
	def getPrice(self, chain_size=-1):
		if chain_size == -1:
			num = len(self.territory)
		else:
			num = chain_size

		# These values are copied from the rules
		if self.lux_level == "low":
			# Is not currently a hotel, stocks have no value
			if num < 2:
				return 0

			if num == 2:
				return 200
			elif num == 3:
				return 300
			elif num == 4:
				return 400
			elif num == 5:
				return 500
			elif num <=10:
				return 600
			elif num <=20:
				return 700
			elif num <= 30:
				return 800
			elif num <=40:
				return 900
			else:
				return 1000
		elif self.lux_level == "med":
			# Is not currently a hotel, stocks have no value
			if num < 2:
				return 0

			if num == 2:
				return 300
			elif num == 3:
				return 400
			elif num == 4:
				return 500
			elif num == 5:
				return 600
			elif num <=10:
				return 700
			elif num <=20:
				return 800
			elif num <= 30:
				return 900
			elif num <=40:
				return 1000
			else:
				return 1000
		elif self.lux_level == "high":
			# Is not currently a hotel, stocks have no value
			if num < 2:
				return 0

			if num == 2:
				return 400
			elif num == 3:
				return 500
			elif num == 4:
				return 600
			elif num == 5:
				return 700
			elif num <=10:
				return 800
			elif num <=20:
				return 900
			elif num <= 30:
				return 1000
			elif num <=40:
				return 1100
			else:
				return 1200

	# If chain_size==-1, user current size of chain
	def getBonuses(self, chain_size=-1):
		if chain_size == -1:
			num = len(self.territory)
		else:
			num = chain_size

		# These values are copied from the rules
		if self.lux_level == "low":
			# Is not currently a hotel, stocks have no value
			if num < 2:
				return 0

			if num == 2:
				return 2000, 1000
			elif num == 3:
				return 3000, 1500
			elif num == 4:
				return 4000, 2000
			elif num == 5:
				return 5000, 2500
			elif num <=10:
				return 6000, 3000
			elif num <=20:
				return 7000, 3500
			elif num <= 30:
				return 8000, 4000
			elif num <=40:
				return 9000, 4500
			else:
				return 10000, 5000
		elif self.lux_level == "med":
			# Is not currently a hotel, stocks have no value
			if num < 2:
				return 0

			if num == 2:
				return 3000, 1500
			elif num == 3:
				return 4000, 2000
			elif num == 4:
				return 5000, 2500
			elif num == 5:
				return 6000, 3000
			elif num <=10:
				return 7000, 3500
			elif num <=20:
				return 8000, 4000
			elif num <= 30:
				return 9000, 4500
			elif num <=40:
				return 10000, 5000
			else:
				return 11000, 5500
		elif self.lux_level == "high":
			# Is not currently a hotel, stocks have no value
			if num < 2:
				return 0

			if num == 2:
				return 4000, 2000
			elif num == 3:
				return 5000, 2500
			elif num == 4:
				return 6000, 3000
			elif num == 5:
				return 7000, 3500
			elif num <=10:
				return 8000, 4000
			elif num <=20:
				return 9000, 4500
			elif num <= 30:
				return 10000, 5000
			elif num <=40:
				return 11000, 5500
			else:
				return 12000, 6000

## Data structure to hold playable game tiles
# The phrase "Tile" is used somewhat inconsistently,
#   for example Board.tiles_remaining uses ordered pairs. TODO
class Tile:
	def __init__(self,value,x,y):
		# Coordinates of corrosponding board location
		self.x = x
		self.y = y
		# Chain that this Tile belongs to. -1 means invalid.
		self.value = value

## Data structure to hold full game board state
class Board:
	def __init__(self, width=12, height=9):
		self.width  = width
		self.height = height

		# -1 means empty, 0 means unaffiliated with chain, 1-6 means part of chain
		self.state = [[-1 for x in xrange(width)] for y in xrange(height)]

		# Initialize 6 chains, for standard Aquire rules.
		# This is a fun parameter to play with
		self.chains = {1:Chain(1),
					   2:Chain(2),
					   3:Chain(3),
					   4:Chain(4),
					   5:Chain(5),
					   6:Chain(6)}

		# Associated color for visualizer to use for each chain.
		# Note: len() must be >= length of self.chains
		self.color_dict = {-1:"w",
							0:"k",
							1:"r",
							2:"y",
							3:"m",
							4:"g",
							5:"b",
							6:"c"}

		# This is the face down tiles to be drawn
		self.tiles_remaining = [(x,y) for x in xrange(width) for y in xrange(height)]
		random.shuffle(self.tiles_remaining)

		self.players = []
		self.gameCompleted = False


	# Remove a tile from self.tiles_remaining and return selected tile
	def drawTile(self):
		if len(self.tiles_remaining)==0:
			print "Out of tiles, game is over"
			self.gameCompleted = True
			return (0,0)

		drawn_tile = self.tiles_remaining[0]
		del self.tiles_remaining[0]
		return drawn_tile

	# Used when founding a new hotel chain. Return available chain
	def getEmptyChain(self, lux_pref):
		# TODO account for lux_pref, for AIs that use that
		for key in self.chains:
			if len(self.chains[key].territory) ==0:
				return key

		# Currently it is up to the AI not to do this, TODO
		raise Exception("Tried to make a chain where no chain was valid")

	## Input:   An ordered pair (x,y)
	## Returns: list of Tiles
	def getSurroundingTiles(self, tile):
		x = tile[0]
		y = tile[1]

		# Edge conditions are so annoying
		# Awkwardly, state is accessed state[y][x] (row, col)
		if x == 0:
			left = Tile(-1,x-1,y,)
		else:
			left = Tile(self.state[y][x-1], x-1,y)

		if x == self.width-1:
			right = Tile(-1,x+1,y)
		else:
			right = Tile(self.state[y][x+1],x+1,y)

		if y == 0:
			top = Tile(-1,x,y-1)
		else:
			top = Tile(self.state[y-1][x],x,y-1)

		if y == self.height-1:
			bottom = Tile(-1,x,y+1)
		else:
			bottom = Tile(self.state[y+1][x],x,y+1)

		return [left,right,top,bottom]

	# Trigger all state update associated with a player playing a tile
	# merge_pref should allow for AI to choose between chains in a merge
	def playTile(self, player, tile, lux_pref="med", merge_pref=-1):
		surrounding_tiles = self.getSurroundingTiles(tile)

		existing_chains = [el for el in surrounding_tiles if el.value > 0]

		# This metric determines if action triggers merge/place/expand
		unique_ecs = list(set([el.value for el in existing_chains]))

		neutral_chains = [el for el in surrounding_tiles if el.value == 0]

		## Add to existing chains
		if len(unique_ecs) == 1:
			# Add to chains the new tile and all neutral tiles connecting it
			merged_tiles = [(el.x,el.y) for el in neutral_chains]
			tiles = [tile]
			tiles.extend(merged_tiles)

			# Grow the chain
			board.chains[existing_chains[0].value].territory.extend(tiles)

			# Update board state
			for t in tiles:
				self.state[t[1]][t[0]] = existing_chains[0].value


		## Merge chains!
		# This assumes merge_pref is valid (i.e. not the smaller chain)
		# TODO Throw an error or otherwise fail action if AI cheats
		elif len(unique_ecs) >= 1:
			print "~~~ Liquidation Sale! ~~~"


			# TODO Allow AI to arbitrate between chains of equal size
			## INSERT AI CHOICE HERE: If chains are equal, which to keep? ##
			chain_strength = sorted(existing_chains, key=lambda chain: len(self.chains[chain.value].territory), reverse=True)
			winner = chain_strength[0].value

			print "Winner is: " + str(winner)
			print " Losers are: "
			liquidation_targets = list(set([el.value for el in existing_chains if el.value != winner]))
			print liquidation_targets

			# TODO allow stock transfers/keeps
			## INSERT AI CHOICE HERE: Keep stocks or sell? ##
			# Liquidate players' shares in acquired companies
			for lt in liquidation_targets:
				first, second = board.chains[lt].getBonuses()
				all_vals = [el.stocks[lt] for el in board.players]
				contenders = [el for el in board.players if el.stocks[lt] > 0]
				contenders = sorted(contenders, key=lambda el:el.stocks[lt], reverse=True)

				if len(contenders) == 0:
					print "This should not occur, worry"
					print all_vals
				if len(contenders) == 1:
					contenders[0].cash += first
					contenders[0].cash += second
				else:
					contenders[0].cash += first
					contenders[1].cash += second

				for player in self.players:
					if player.stocks[lt] >0:
						player.cash += player.stocks[lt]*board.chains[lt].getPrice()
						player.stocks[lt] = 0

			tiles = [tile]
			merged_tiles = [(el.x,el.y) for el in neutral_chains]
			tiles.extend(merged_tiles)
			for chain in unique_ecs:
				if chain != winner:
					# Absorb assets into winner
					tiles.extend(self.chains[chain].territory)

					print "Liquidating "+str(chain)

					# Reset the chain in board state
					self.chains[chain] = Chain(chain)

			# Grow the chain
			board.chains[winner].territory.extend(tiles)

			# Update board state
			for t in tiles:
				self.state[t[1]][t[0]] = winner

		## Found a new chain
		# TODO Need to enforce that there's a chain available. Do I do this?
		elif len(neutral_chains) > 0:
			# Added tiles will be the new tile and all neutral tiles connecting it
			merged_tiles = [(el.x,el.y) for el in neutral_chains]
			tiles = [tile]
			tiles.extend(merged_tiles)

			## INSERT AI CHOICE HERE: What Lux Pref for chain creation? ##
			new_chain = self.getEmptyChain(lux_pref)

			player.stocks[new_chain] += 1

			# Populate the new chain with it's claimed tiles
			self.chains[new_chain].territory.extend(tiles)

			# Update board state
			for t in tiles:
				self.state[t[1]][t[0]] = new_chain

		# If none of the above events happen, just place a neutral tile
		else:
			self.state[tile[1]][tile[0]] = 0


	# Returns dictionary of key:chain value: # of stocks free to purchase
	def getAvailableStocks(self):
		available_stocks = {1:26, 2:26, 3:26, 4:26, 5:26, 6:26}
		for player in self.players:
			for key in player.stocks:
				available_stocks[key] -= player.stocks[key]

		return available_stocks


## TODO create an AI class and give them hooks into
##      anything commented "INSERT AI CHOICE HERE"
## Data structure to maintain game state for a player
class Player:
	def __init__(self, uid, board):
		self.uid = uid
		self.cash = 6000

		# This is a pointer to an object
		self.board = board

		self.cash_history = [self.cash]
		self.net_asset_history = [self.cash]

		# Populate tiles
		self.tiles = []
		for i in xrange(6):
			self.tiles.append(board.drawTile())

		# Key: Chain UID, Value: # of shares
		self.stocks = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}

	# Return list of all tiles this player is allowed to play
	def getValidPlays(self):
		valid_plays = []
		for tile in self.tiles:
			surrounding_tiles = self.board.getSurroundingTiles(tile)
			existing_chains = [el for el in surrounding_tiles if el.value > 0]
			unique_ecs = list(set([el.value for el in existing_chains]))
			neutral_chains = [el for el in surrounding_tiles if el.value == 0]

			# TODO verify "safe chains" game mechanic works in practice
			if len(unique_ecs) == 1:
				valid_plays.append(tile)
			elif len(unique_ecs) >= 2:
				sizes = [len(self.board.chains[el].territory) for el in unique_ecs]
				safe_chains = [el for el in sizes if el >=11]
				# There is a chain that is not a safe chain
				if len(safe_chains) <=1:
					valid_plays.append(tile)
			elif len(neutral_chains) == 0:
				valid_plays.append(tile)
			else:
				# If there is a chain not yet established
				if len([el for el in board.chains if len(board.chains[el].territory)==0]) > 0:
					valid_plays.append(tile)
		return valid_plays

	# Returns total wealth of player. Can be used for AI decisions or determining winners
	def getNetAssets(self):
		total = 0

		# Account for cash in hand
		total += self.cash

		# Account for stock assets
		for key in self.stocks:
			total += self.stocks[key]*self.board.chains[key].getPrice()

		return total

	# TODO Who should regulate that the stock purchases are legal?
	# I want to abstract that away from the AIs if possible
	# Trigger the purchase of a stock for this player
	def purchaseStocks(self):
		available_stocks = self.board.getAvailableStocks()

		## INSERT AI CHOICE HERE: Stock purchase selection ##
		# For now, just purchase a random amount of a random chain
		purchase_number = int(1.5+random.random()*1.49)
		purchase_uid    = int(1+random.random()*5.1)

		price_per_share = self.board.chains[purchase_uid].getPrice()

		if purchase_number*price_per_share <= self.cash:
			self.cash -= purchase_number*price_per_share
			self.stocks[purchase_uid] += purchase_number


#### Run a simulation of the game! ####

# Initialize board
board = Board()
grid = plt.GridSpec(2, 4, wspace=0.5, hspace=0.5)

# Visualization function for board
def showBoard():
	# TODO pass args correctly though drawnow
	global board
	global grid


	plt.subplot(grid[0:, 0:2])

	packed_state = {-1: [], 0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[]}
	for y in xrange(board.height):
		for x in xrange(board.width):
			packed_state[board.state[y][x]].append((x,y))

	#plt.clf()
	for key in packed_state:
		if key != -1:
			color = board.color_dict[key]

			xs = [el[0] for el in packed_state[key]]
			ys = [el[1] for el in packed_state[key]]

			plt.plot([xs],[ys],color+"o", ms=30.0)
			plt.title("Aquire Board State")
			plt.xlim([-1,board.width])
			plt.ylim([-1,board.height])

	# TODO Generalize this to N players
	# (Just suppress these plots if playing with N!=4)
	#p1
	plt.subplot(grid[0, 2])
	plt.plot(board.players[0].cash_history, "k--")
	plt.plot(board.players[0].net_asset_history, "b")
	plt.title("Player 1 assets (net and cash)")

	#p2
	plt.subplot(grid[0, 3])
	plt.plot(board.players[1].cash_history, "k--")
	plt.plot(board.players[1].net_asset_history, "b")
	plt.title("Player 2 assets (net and cash)")


	#p3
	plt.subplot(grid[1, 2])
	plt.plot(board.players[2].cash_history, "k--")
	plt.plot(board.players[2].net_asset_history, "b")
	plt.title("Player 3 assets (net and cash)")

	#p4
	plt.subplot(grid[1, 3])
	plt.plot(board.players[3].cash_history, "k--")
	plt.plot(board.players[3].net_asset_history, "b")
	plt.title("Player 4 assets (net and cash)")




# Initialize players
p1 = Player(1, board)
p2 = Player(2, board)
p3 = Player(3, board)
p4 = Player(4, board)

board.players.extend([p1,p2,p3,p4])


drawnow.figure(figsize=(13, 5))

# Play the game!
while not board.gameCompleted:
	for player in board.players:
		## Play tile
		possible_tiles = player.getValidPlays()
		if len(possible_tiles) >=1:

			### INSERT AI CHOICE HERE: Which tile to play ###
			# For now, choose the first valid tile
			chosen_play = possible_tiles[0]
			player.tiles.remove(chosen_play)
			board.playTile(player, chosen_play)

		## Buy stocks
		player.purchaseStocks()

		## Draw tile
		player.tiles.append(board.drawTile())

		## Update player state
		player.cash_history.append(player.cash)
		player.net_asset_history.append(player.getNetAssets())

		## Display board
		drawnow.drawnow(showBoard)

		# Check if game completion
		for key in board.chains:
			if len(board.chains[key].territory)>=41:
				board.gameCompleted = True;

time.sleep(500)
