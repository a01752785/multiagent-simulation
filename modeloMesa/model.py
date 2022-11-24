from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agent import *
from random import choice
import json


class Node():
    neighbours = []

    def __init__(self):
        self.neighbours = []

    def addNeighbour(neighbour):
        self.neighbours.append(neighbour)


class MapConnections():
    connections = {}
    
    def __init__(self):
        self.connections = {}
        
    def addNodes(self, coord, nodes):
        self.connections[coord] = nodes


class RandomModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
    """
    def __init__(self, N):

        dataDictionary = json.load(open("mapDictionary.json"))
        self.destinos = []
        self.mapa = MapConnections()
        self.traffic_lights = []
        self.num_agents = N
        self.running = True

        with open('2022_base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)

            self.grid = MultiGrid(self.width, self.height, torus = False) 
            self.schedule = RandomActivation(self)

            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<"]:
                        agent = Road(f"r_{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col in ["R", "r", "L", "l", "U", "u", "D", "d"]:
                        agent = Traffic_Light(f"tl_{r*self.width+c}", self, False if col.isupper() else True, int(dataDictionary[col][0]), dataDictionary[col][1])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.traffic_lights.append(agent)

                    elif col == "#":
                        agent = Obstacle(f"ob_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col == ".":
                        agent = Destination(f"d_{r*self.width+c}", self)
                        self.destinos.append((c, self.height - r - 1))
                        self.grid.place_agent(agent, (c, self.height - r - 1))

            self.build_graph()
            id = 1000
            while id < self.num_agents + 1000:
                agent = Car(id, choice(self.destinos), self)
                self.grid.place_agent(agent, choice(self.destinos))
                self.schedule.add(agent)
                id = id + 1

        

    def step(self):
        '''Advance the model by one step.'''
        if self.schedule.steps % 10 == 0:
            for agent in self.traffic_lights:
                agent.state = not agent.state
        self.schedule.step()

    def getNeighbours(self, coords):
        neighbours = []
        cells = self.grid.get_cell_list_contents([coords])   
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        str_dir_to_coords = {"Down": directions[3],
                             "Up": directions[2],
                             "Right": directions[0],
                             "Left": directions[1]}
        for cell in cells:
            if isinstance(cell, Destination):
                for dir_row, dir_col in directions:
                    new_coord = (coords[0] + dir_row, coords[1] + dir_col)
                    if new_coord[0] < 0 or new_coord[1] < 0:
                        continue
                    if new_coord[0] >= self.width or new_coord[1] >= self.height:
                        continue
                    cellsRowMinus = self.grid.get_cell_list_contents([new_coord])
                    for cellRowMin in cellsRowMinus:
                        if not isinstance(cellRowMin, Obstacle):
                            neighbours.append(new_coord)
    
            elif isinstance(cell, Road):
                for dir_row, dir_col in directions:
                    new_coord = (coords[0] + dir_row, coords[1] + dir_col)
                    if new_coord[0] < 0 or new_coord[1] < 0:
                        continue
                    if new_coord[0] >= self.width or new_coord[1] >= self.height:
                        continue
                    if cell.direction == "Left" and dir_row == 1:
                        continue
                    if cell.direction == "Right" and dir_row == -1:
                        continue
                    if cell.direction == "Up" and dir_col == -1:
                        continue
                    if cell.direction == "Down" and dir_col == 1:
                        continue
                    cellsRowMinus = self.grid.get_cell_list_contents([new_coord])
                    for cellRowMin in cellsRowMinus:
                        if not isinstance(cellRowMin, Obstacle):
                            neighbours.append(new_coord)
            elif isinstance(cell, Traffic_Light):
                for dir_row, dir_col in directions:
                    new_coord = (coords[0] + dir_row, coords[1] + dir_col)
                    if new_coord[0] < 0 or new_coord[1] < 0:
                        continue
                    if new_coord[0] >= self.width or new_coord[1] >= self.height:
                        continue
                    # Semaforo solo se puede mover en su propia direccion
                    if str_dir_to_coords[cell.direction] == (dir_row, dir_col):
                        cellsRowMinus = self.grid.get_cell_list_contents([new_coord])
                        for cellRowMin in cellsRowMinus:
                            if not isinstance(cellRowMin, Obstacle):
                                neighbours.append(new_coord)
        return neighbours

    def build_graph(self):
        for row in range(self.width):
            for col in range(self.height):
                agents = self.grid.get_cell_list_contents([(row, col)])
                for agent in agents:
                    if isinstance(agent, Obstacle):
                        continue
                    directions = self.getNeighbours((row, col))
                    self.mapa.addNodes((row, col), directions)