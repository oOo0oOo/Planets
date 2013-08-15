import random

class Planet(object):
	def __init__(self, ind, color = 0):
		self.color = color
		self.ind = ind

		self.player = False
		self.number = False
		self.neighbours = []

	def invade(self, player, number):
		if player == self.player:
			self.number += number
		else:
			self.number -= number
			if self.number < 0:
				self.player = player
				self.number = abs(self.number)

	def remove(self, player, number, color):
		pl = [i for i, n in enumerate(self.neighbours) if n.color == color]

		if pl:
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
	def __init__(self, ind, home_planet, life):
		self.ind = ind
		self.life = life
		self.home_planet = home_planet
		self.current_planet = home_planet


class Game(object):
	def __init__(self):
		self.players = {}
		self.planets = {}
		self.planet_graph = False

	def add_player(self, home_planet, life = 5):
		k = self.players.keys()
		for i in range(1, 100):
			if i not in k:
				break

		self.players[i] = Player(i, home_planet, life)

		self.planets[home_planet].player = i
		self.planets[home_planet].number = 0


	def load_planets(self, planet_graph):
		self.planet_graph = planet_graph
		for planet in planet_graph.keys():
			self.planets[planet] = Planet(planet)

		for pl, con in planet_graph.items():
			for ne in con:
				self.planets[pl].neighbours.append(self.planets[ne])

	def find_colors(self, max_colors, max_tries = 50000):
		colors = range(1, max_colors+1)
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
				if len(list(set(n_colors))) != len(n_colors):
					break
			else:
				found = True

		if found:
			for p, c in planets.items():
				self.planets[p].color = c
			print 'Found colors in {} tries'.format(tries)
		else:
			print 'Could not find colors in {} tries'.format(tries)

	def plot_planets(self):
		import networkx as nx
		import matplotlib.pyplot as plt

		graph = nx.Graph()

		edge_list = []
		for g, n in self.planet_graph.items():
			for nei in n:
				edge_list.append((g, nei))

		graph.add_edges_from(edge_list)

		colors = [self.planets[n].color for n in sorted(self.planets.keys())]

		# Create labels
		labels = {}
		for i, pl in self.planets.items():
			if pl.player:
				labels[i] = '{}: Player {} ({})'.format(i, pl.player, pl.number)
			else:
				labels[i] = str(i)

		nx.draw_networkx(graph, node_color = colors, labels = labels)
		plt.show()
