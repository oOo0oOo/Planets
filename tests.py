import unittest
import time
import engine_simple

class TestSimpleEngine(unittest.TestCase):
	def test_game_setup(self):
		planet_graph = {1: [2,3], 2: [1, 3, 5],
			3: [1, 2, 4], 4: [3, 5, 8], 5: [2, 4, 6, 7], 
			6: [5, 7, 11], 7: [6, 8, 9, 5], 8: [4, 7, 10],
			9: [7, 10, 11], 10: [8, 9], 11: [6, 9]
			}

		game = engine_simple.Game()
		game.load_planets(planet_graph)
		game.find_colors(4)

		game.add_player(1)
		game.add_player(11)

		game.planets[3].invade(1, 3)
		game.planets[8].invade(2, 3)

		game.plot_planets()


if __name__ == '__main__':
	unittest.main()