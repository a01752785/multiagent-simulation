from mesa import Agent
from collections import deque


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
        self.momentsDirection = ["Left", "Up", "Right"]
        self.mapa = self.model.mapa
        self.route = deque()

    def compute_route(self, destination):
        visited = set()
        visited.add(self.pos)
        dist = {self.pos : 0}
        parent = {}
        queue = deque()
        queue.append(self.pos)
        while len(queue):
            position = queue.popleft()
            for next_position in self.mapa.connections[position]:
                if next_position not in visited:
                    visited.add(next_position)
                    queue.append(next_position)
                    dist[next_position] = dist[position] + 1
                    parent[next_position] = position

        current_position = destination
        route = []
        while current_position != self.pos:
            route.append(current_position)
            current_position = parent[current_position]
        route.reverse()
        return deque(route)

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
            self.posibleMovements = [((x-1,y), "Right"),((x,y+1), "Down"),((x+1,y), "Left")]
            y += 1
        elif direction == "Down":
            self.posibleMovements = [((x+1,y), "Left"),((x,y-1), "Up"),((x-1,y), "Right")]
            y -= 1
        elif direction == "Left":
            self.posibleMovements = [((x,y-1), "Right"),((x-1,y), "Right"),((x,y+1), "Down")]
            x -= 1
        elif direction == "Right":
            self.posibleMovements = [((x,y+1), "Down"),((x+1,y), "Left"),((x,y-1), "Up")]
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
        distancia_minima = 1000
        for pos in self.posibleMovements:
            if pos[0][0] < self.model.width and pos[0][1] < self.model.height:
                content = self.model.grid.get_cell_list_contents([pos[0]])
                # (isinstance(cell, Road) and ((cell.direction != self.direction and cell.direction == pos[1]) or cell.direction == self.direction))
                for cell in content:
                    if (isinstance(cell, Road) and ((cell.direction != self.direction and cell.direction != pos[1]) 
                    or cell.direction == self.direction)) or isinstance(cell, Destination) and pos[0] == self.destino:
                        distancia_nueva = self.calcularDistancia(self.destino, pos[0])
                        if distancia_nueva < distancia_minima:
                            distancia_minima = distancia_nueva
                            new_position =  pos[0]
                        elif distancia_nueva == distancia_minima and (self.pos != (1,10) or self.pos != (1,9)):
                            new_position = self.posibleMovements[1][0]

            else:
                new_position = self.posibleMovements[1][0]
        return new_position

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        if self.pos == self.destino:
            new_position = self.pos
            self.isInDestiny = True

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
                        new_position = self.route.popleft()

            elif isinstance(cell, Traffic_Light):
                new_position = self.route.popleft()
    
        self.model.grid.move_agent(self, new_position)

    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        if len(self.route) == 0:
            self.route = self.compute_route(self.destino)
        self.move()
    

class Traffic_Light(Agent):
    """
    Traffic light. Where the traffic lights are in the grid.
    """
    def __init__(self, unique_id, model, state = False, timeToChange = 10, direction = "Left"):
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
        self.direction = direction

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
