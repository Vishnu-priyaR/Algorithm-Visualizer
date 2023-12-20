import pygame
from queue import PriorityQueue
#Prioirty Queues are used for storing G(n) values in it's open set

pygame.init()   #command to get screen
#Screen Size
scn = pygame.display.set_mode((600, 600))
pygame.display.set_caption("SHORTEST PATH using A* Algorithm")

#set image
#use 32 x 32 pixels
#icon = pygame.image.load('ufo.jpg')#icon
#pygame.display.set_icon(icon)  

#colour codes
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)
ORANGE = (255, 165 ,0)
PURPLE = (128, 0, 128)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
NEON = (127,255,0)

#Function to draw
def draw(scn, grid, rows, width):
	scn.fill(WHITE)

	for row in grid:
		for cube in row:
			cube.draw(scn)

	draw_grid(scn, rows, width)
	pygame.display.update()

#Function to get coordinate
def get_the_clicked_pos(pos, rows, width):
	gap = width // rows
	i,j = pos

	row = i // gap
	column = j // gap

	return row, column

#50x50 grid is constructed with each position 
#known as cubes which is made as class
class Cube:
    #colours are needed to diff between source cube
    #destination cube and hinderance cube
	def __init__(self, row, column, width, total_rows):
		self.row = row
		self.column = column
		self.x = row * width       #coordinate of x
		self.y = column * width    #coordinate of y
		self.colour = WHITE        #width of cube = screensize/total number of cubes                                   
        #all the cubes are set white
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.column

#FUNCTIONS to make the check the colour of CUBE
#cube being closed i.e. already visited cube
	def chk_start(self):
		return self.colour == ORANGE

	def chk_end(self):
		return self.colour == RED

	def chk_open(self):
		return self.colour == GREY

	def chk_closed(self):
		return self.colour == PURPLE

    #wall is black in colour
	def chk_Wall(self):
		return self.colour == BLACK

    #is a cube is choosed and later unchoosen
    #it's colour becomes white
	def reset(self):
		self.colour = WHITE

#FUNCTIONS to make the cube assign colour
	def put_start(self):
		self.colour = ORANGE

	def put_end(self):
		self.colour = RED

	def put_open(self):
		self.colour = GREY

	def put_closed(self):
		self.colour = PURPLE

	def put_Wall(self):
		self.colour = BLACK

	def put_path(self):
		self.colour = NEON

	def draw(self, scn):
		pygame.draw.rect(scn, self.colour, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
        #DOWN
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.column].chk_Wall(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.column])

        #UP
		if self.row > 0 and not grid[self.row - 1][self.column].chk_Wall(): # UP
			self.neighbors.append(grid[self.row - 1][self.column])

        #RIGHT
		if self.column < self.total_rows - 1 and not grid[self.row][self.column + 1].chk_Wall(): # RIGHT
			self.neighbors.append(grid[self.row][self.column + 1])

        #LEFT
		if self.row > 0 and not grid[self.row][self.column - 1].chk_Wall(): # LEFT
			self.neighbors.append(grid[self.row][self.column - 1])

	#def __lt__(self, other):
		#return False

#heuristic funtion
#Manhattan distance or taxi cab distance is calculated
"""The sum of the lengths of the projections of the line segment between the points onto the coordinate axes.
Or, it is the sum of absolute difference between the measures in all dimensions of two points.
"""
def heuristic(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x2 - x1) + abs(y2 - y1)


def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.put_path()
		draw()

#algorithm function
def algo(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
    #adding start and it's F(n)
	open_set.put((0, count, start))
	came_from = {}
    #holds value of G(n)
    #initially infinity
	g_score = {cube: float("inf") for row in grid for cube in row}
	g_score[start] = 0
    #holds value of F(n)
    #initially infinity
	f_score = {cube: float("inf") for row in grid for cube in row}
	f_score[start] = heuristic(start.get_pos(), end.get_pos())

    #a set variable is created to ensure that
    #the element is there in the queue or not
	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
            #path is being made
			reconstruct_path(came_from, end, draw)
			end.put_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count = count + 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.put_open()

		draw()

		if current != start:
			current.put_closed()

	return False

#A function to make the grid is created by 
#using an object of Cube class
#here column is not taken as seperate parameter
#as number of columns = number of rows
def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(0, rows):
		grid.append([])
		for j in range(0, rows):
			cube = Cube(i, j, gap, rows)
			grid[i].append(cube)

	return grid

#A function to draw the created grid
#here column is not taken as seperate parameter
#as number of columns = number of rows
def draw_grid(scn, rows, width):
	gap = width // rows
	for i in range(0, rows):
        #horizontal line is drawn for each 
        #cube differentiation
		pygame.draw.line(scn, BLACK, (0, i * gap), (width, i * gap))
		for j in range(0, rows):
			pygame.draw.line(scn, BLACK, (j * gap, 0), (j * gap, width))

def main(scn, width):
    #lets define the events of the game
	ROWS = COLUMNS = 50
	grid = make_grid(ROWS, width)
    #declaring variable for knwing whether
    #game has started or algorithm is done
    
	start = end = None
    #started = False
	run = True
	while run:
		draw(scn, grid, ROWS, width)
        #all the events are checked using pygame.event.get()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

            #checks whether the left side 
            #or right side of mouse is pressed
			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, column = get_the_clicked_pos(pos, ROWS, width)
				cube = grid[row][column]
				if not start and cube != end:
					start = cube
					start.put_start()

				elif not end and cube != start:
					end = cube
					end.put_end()

				elif cube != end and cube != start:
					cube.put_Wall()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, column = get_the_clicked_pos(pos, ROWS, width)
				cube = grid[row][column]
				cube.reset()
				if cube == start:
					start = None
				elif cube == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for cube in row:
							cube.update_neighbors(grid)

					algo(lambda: draw(scn, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

main(scn, 600)
