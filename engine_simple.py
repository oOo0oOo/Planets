import random

class Planet(object):
	'''
		Planet: Node in graph with associated color and neighbours.
		Units can invade a planet or be removed from one.

		When a player has more than one unit on the planet it will belong to the player.

	'''
	def __init__(self, ind, color = 0):
		self.color = color
		self.ind = ind

		self.player = False
		self.number = False
		self.neighbours = []

	def invade(self, player, number):
		'''
			Invade a planet. If planet already belongs invading player the number is simply added.
			Otherwise the player will decimate the units already on the planet and will take over
			the planet if posssible.

		'''

		if player == self.player:
			self.number += number
		else:
			self.number -= number
			if self.number < 0:
				self.player = player
				self.number = abs(self.number)

	def remove(self, player, number, color):
		'''
			Remove a number of units from planet. Units can only be removed if they invade another planet.
			(This is coded in the planet color.)

		'''
		pl = [i for i, n in enumerate(self.neighbours) if n.color == color]

		# Invade other planet if color exists in neighbours and correct player
		if pl and self.player == player:

			ind = pl[0]
			if number >= self.number:
				number = self.number
				self.number = 0
				self.player = False
			else:
				self.number -= number

			self.neighbours[ind].invade(player, number)
		else:
			print 'Impossible move...'


class Player(object):
	'''
		Not much more than a data structure...

	'''
	def __init__(self, ind, home_planet, life):
		self.ind = ind
		self.life = life
		self.home_planet = home_planet
		self.current_planet = home_planet


class Game(object):
	'''
		Running all the game mechanics.

	'''
	def __init__(self):
		self.players = {}
		self.planets = {}
		self.planet_graph = False

	def add_player(self, home_planet, life = 5):
		'''
			Add a player to the game. Will automatically get the lowest index assigned.
			home_planet is the index of the players home planet (starting point).

		'''
		# Find min possible key (with a max of 100)
		k = self.players.keys()
		for i in range(1, 100):
			if i not in k:
				break

		self.players[i] = Player(i, home_planet, life)

		self.planets[home_planet].player = i
		self.planets[home_planet].number = 0


	def load_planets(self, planet_graph):
		'''
			Load planets from planet graph.
			planet_graph is a dict with nodes as keys and a list of edges as values: 
			planet_graph = {1: [2,3], 2: [1, 3], ...}

		'''
		# Create planets
		self.planet_graph = planet_graph
		for planet in planet_graph.keys():
			self.planets[planet] = Planet(planet)

		# Add neighbours to each planet
		for pl, con in planet_graph.items():
			for ne in con:
				self.planets[pl].neighbours.append(self.planets[ne])

	def find_colors(self, num_colors, max_tries = 50000):
		'''
			Find a color scheme where each planets neighbours have all different colors.
			num_colors is the number of colors that can be used,
			max_tries is the maximum number of tries to find a configuration.

		'''
		colors = range(1, num_colors+1)
		found = False
		tries = 0

		while not found and tries < max_tries:
			tries += 1
			# Use random colors
			planets = {k: random.choice(colors) for k in self.planet_graph.keys()}

			# Check if ok conf
			for p, c in planets.items():
				# Get colors of all neighbour planets
				n_colors = [planets[n] for n in self.planet_graph[p]]
				# Not ok if duplicate colors exist
				if len(set(n_colors)) != len(n_colors):
					break
			else:
				found = True

		# Assign colors if found
		if found:
			for p, c in planets.items():
				self.planets[p].color = c
			print 'Found colors in {} tries'.format(tries)
		else:
			print 'Could not find colors in {} tries'.format(tries)

	def plot_planets(self):
		'''
			Plot connections, color, and occupancy of all the planets as a graph.
			This function uses non standard library modules: networkx and matplotlib

		'''
		import networkx as nx
		import matplotlib.pyplot as plt

		graph = nx.Graph()

		# Create edge list and add edges
		edge_list = []
		for g, n in self.planet_graph.items():
			for nei in n:
				edge_list.append((g, nei))
		graph.add_edges_from(edge_list)

		# Create list with colors of planets
		colors = [self.planets[n].color for n in sorted(self.planets.keys())]

		# Create label list
		labels = {}
		for i, pl in self.planets.items():
			if pl.player:
				labels[i] = '{}: Player {} ({})'.format(i, pl.player, pl.number)
			else:
				labels[i] = str(i)

		# Draw and show plot
		nx.draw_networkx(graph, node_color = colors, labels = labels)
		plt.show()
