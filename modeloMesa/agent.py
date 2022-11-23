from mesa import Agent

class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, destino, model):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.isInDestiny = False
        self.direction = ""
        self.destino = destino
        self.posibleMovements = []

    def moveLeaveStart(self):
        """ 
        Mueve al agente al camino
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False)
        
        for movement in possible_steps:
            cellmates = self.model.grid.get_cell_list_contents([movement])
            for element in cellmates:
                if isinstance(element, Road):
                    return(movement)

    def moveToDirection(self, direction):
        x, y = self.pos
        if direction == "Up":
            self.posibleMovements = [(x-1,y),(x,y+1),(x+1,y)]
            y += 1
        elif direction == "Down":
            self.posibleMovements = [(x+1,y),(x,y-1),(x-1,y)]
            y -= 1
        elif direction == "Left":
            self.posibleMovements = [(x,y+1),(x-1,y),(x,y-1)]
            x -= 1
        elif direction == "Right":
            self.posibleMovements = [(x,y-1),(x+1,y),(x,y+1)]
            x += 1
        return(x, y)

    def calcularDistancia(self, posDestino, posAMover):
        """
        Es el calculo de una distancia dada dos posiciones
        """
        nx, ny = posDestino
        ax, ay = posAMover
        return (abs(ax - nx) + abs(ay - ny))

    def moveIntelligent(self):
        new_position = self.pos
        print(new_position)
        distancia_minima = 1000
        for pos in self.posibleMovements:
            content = self.model.grid.get_cell_list_contents([pos])
            for cell in content:
                if isinstance(cell, Road) or isinstance(cell, Destination):
                    distancia_nueva = self.calcularDistancia(self.destino, pos)
                    if distancia_nueva < distancia_minima:
                        distancia_minima = distancia_nueva
                        new_position =  pos
        print(new_position)
        return new_position

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        if self.pos == self.destino:
            new_position = self.pos

        currentCell = self.model.grid.get_cell_list_contents([self.pos])
        for cell in currentCell:
            if isinstance(cell, Destination) and (self.pos != self.destino):
                new_position = self.moveLeaveStart()

            elif isinstance(cell, Road):
                self.direction = cell.direction
                new_position = self.moveToDirection(self.direction)

                # posCellInFront = self.moveToDirection(self.direction)
                contentCellInFront = self.model.grid.get_cell_list_contents([new_position])

                for cellFront in contentCellInFront:
                    if isinstance(cellFront, Traffic_Light):
                        if cellFront.state == False:
                            new_position = self.pos
                    elif isinstance(cellFront, Car):
                        new_position = self.pos
                    elif isinstance(cellFront, Road):
                        new_position = self.moveIntelligent()

            elif isinstance(cell, Traffic_Light):
                new_position = self.moveToDirection(self.direction)
        
        self.model.grid.move_agent(self, new_position)

    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        self.move()
        

class Traffic_Light(Agent):
    """
    Traffic light. Where the traffic lights are in the grid.
    """
    def __init__(self, unique_id, model, state = False, timeToChange = 10):
        super().__init__(unique_id, model)
        """
        Creates a new Traffic light.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            state: Whether the traffic light is green or red
            timeToChange: After how many step should the traffic light change color 
        """
        self.state = state
        self.timeToChange = timeToChange

    def step(self):
        """ 
        To change the state (green or red) of the traffic light in case you consider the time to change of each traffic light.
        """
        # if self.model.schedule.steps % self.timeToChange == 0:
        #     self.state = not self.state
        pass

class Destination(Agent):
    """
    Destination agent. Where each car should go.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Obstacle(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Road(Agent):
    """
    Road agent. Determines where the cars can move, and in which direction.
    """
    def __init__(self, unique_id, model, direction= "Left"):
        """
        Creates a new road.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            direction: Direction where the cars can move
        """
        super().__init__(unique_id, model)
        self.direction = direction

    def step(self):
        pass
