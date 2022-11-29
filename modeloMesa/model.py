#----------------------------------------------------------
# Evidencia 2. Actividad Integradora
# Este programa representa una ciudad donde circulan carros
# 
# Date: 25-Nov-2022
# Authors:
#           Eduardo Joel Cortez Valente A01746664
#           Paulo Ogando Gulias A01751587
#           David Damián Galán A01752785
#           José Ángel García Gómez A01745865
#----------------------------------------------------------

from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agent import *
from random import choice
import json

class CityModel(Model):
    """ 
    Crea el modelo de la ciudad con los agentes automovil y semaforo.
    Args:
        N: Number of agents in the simulation
    """
    def __init__(self, N):

        dataDictionary = json.load(open("mapDictionary.json"))
        self.destinos = []
        self.num_agents = N
        self.running = True

        self.traffic_lights = []

        with open('2022_base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)

            self.grid = MultiGrid(self.width, self.height, torus = False) 
            self.schedule = RandomActivation(self)
            agentTlc = Traffic_Light_Controller(f"tlc_1", self)
            self.schedule.add(agentTlc)


            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<"]:
                        agent = Road(f"r_{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col in ["S", "s"]:
                        agent = Traffic_Light(f"tl_{r*self.width+c}", self, False if col == "S" else True, int(dataDictionary[col]))
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.traffic_lights.append(agent)
                        if col == "S":
                            agentTlc.add_semaphore(agent, 0)
                        elif col == "s":
                            agentTlc.add_semaphore(agent, 1)
                        

                    elif col == "#":
                        agent = Obstacle(f"ob_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col == "D":
                        agent = Destination(f"d_{r*self.width+c}", self)
                        self.destinos.append((c, self.height - r - 1))
                        self.grid.place_agent(agent, (c, self.height - r - 1))
            
            item = 1000
            while item < 1000 + self.num_agents:
                agent = Car(item, choice(self.destinos), self)
                self.grid.place_agent(agent, choice(self.destinos))
                self.schedule.add(agent)
                item += 1


    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        
