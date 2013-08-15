import cProfile as profile
import random
import time

planet_graph = {1: [2,3], 2: [1, 3, 5],
	3: [1, 2, 4], 4: [3, 5, 8], 5: [2, 4, 6, 7], 
	6: [5, 7, 11], 7: [6, 8, 9, 5], 8: [4, 7, 10],
	9: [7, 10, 11], 10: [8, 9], 11: [6, 9]
	}

def lots(col, num = 100):
	for i in range(num):
		find_colors(col)

def find_colors(max_colors, max_tries = 50000):
	max_colors += 1
	colors = range(1, max_colors)
	found = False
	tries = 0

	#before = time.time()

	while not found and tries < max_tries:
		tries += 1

		# FIX: This line takes by far the most time... (ca. 50-60%)
		planets = {k: random.choice(colors) for k in planet_graph}

		# Check if ok conf
		for p, c in planets.items():
			# Get colors of all neighbour planets
			n_colors = [planets[n] for n in planet_graph[p]]
			if len(set(n_colors)) != len(n_colors):
				break
		else:
			found = True

	#t = time.time()-before
	#print 'Total:', tries, 'Time:', t, 'Tries per s:', (tries/t)

if __name__ == '__main__':
	profile.run('lots(4, 10)')