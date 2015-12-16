#!/bin/env python3

from life_renderer import LifeWindow
from random import randint

ROWS, COLS = 80, 15
cells = [[]]

def printall():
	global cells
	for i in range(ROWS):
		for j in range(COLS):
			if cells[i][j] > 0:
				print((i, j, cells[i][j]))


def setup(life_window):
	global cells
	cells = [[0 for r in range(COLS)] for c in range(ROWS)]
	cells[ROWS // 3 - 1][COLS // 2 - 1] = 1

	life_window.clear_grid()


def loop(life_window):
	life_window.clear_grid()
	global cells
	final_cells = [row[:] for row in cells]

	# Uncomment next line for strange undiscovered fractal
	#final_cells = cells[:]
	for i in range(ROWS):
		for j in range(COLS):
			cell = (i, j)
			neighbor_num = 0
			for neighbor in list(__get_neighbors__(cell, cells, True).values()):
				if neighbor > 0:
					neighbor_num += 1
			if neighbor_num == 1 or neighbor_num == 3 or neighbor_num == 6 or cells[i][j] > 0:
				final_cells[i][j] = cells[i][j] % 8 + 1
			else:
				final_cells[i][j] = 0
	print("Performed automata calculations.")

	cells = final_cells
	for i in range(ROWS):
		for j in range(COLS):
			if cells[i][j] > 0:
				life_window.create_cell(i, j, value = cells[i][j])
	print('Added cells')


def __get_macroblock__(pos, cells):
	neighbor_sum = 0
	neighbors = list(__get_neighbors__(pos, cells, False).values())
	for neighbor in neighbors:
		neighbor_sum += neighbor
	return neighbor_sum // len(neighbors)


def __get_neighbors__(pos, cells, only_living = False):
	positions = []

	even_row, odd_row, even_col, odd_col = pos[0] % 2 == 0, pos[0] % 2 == 1, pos[1] % 2 == 0, pos[1] % 2 == 1

	if ((even_row and even_col) or (odd_row and even_col)):
		positions = [(pos[0] - 1, pos[1]), (pos[0] + 1, pos[1]), (pos[0], pos[1] - 1), \
			(pos[0], pos[1] + 1), (pos[0] + 1, pos[1] - 1), (pos[0] + 1, pos[1] + 1)]
	else:
		positions = [(pos[0] - 1, pos[1]), (pos[0] + 1, pos[1]), (pos[0], pos[1] - 1), \
			(pos[0], pos[1] + 1), (pos[0] - 1, pos[1] - 1), (pos[0] - 1, pos[1] + 1)]

	new_positions = []
	for p in positions:
		if not (p[0] < 0 or p[0] >= ROWS or p[1] < 0 or p[1] >= COLS):
			new_positions.append(p)
	positions = new_positions

	neighbors = {}
	for p in positions:
		if cells[p[0]][p[1]] > 0:
			neighbors[p] = cells[p[0]][p[1]]
		elif not only_living:
			neighbors[p] = 0
	return neighbors


life_window = LifeWindow(ROWS, COLS, setup = setup, loop = loop, hexagonal = True)