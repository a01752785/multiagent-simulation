#----------------------------------------------------------
# Evidencia 2. Actividad Integradora
# Este programa representa a los agentes Car, Trafic Light
# y construlle los objetos Road, Obstacle y Destiny
# 
# Date: 25-Nov-2022
# Authors:
#           Eduardo Joel Cortez Valente A01746664
#           Paulo Ogando Gulias A01751587
#           David Damián Galán A01752785
#           José Ángel García Gómez A01745865
#----------------------------------------------------------


from mesa import Agent

class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: La dirección a la que se movera según la casilla en la que se encuentra
    """
    def __init__(self, unique_id, destino, model):
        """
        Creates a new Car agent.
        Args:
            unique_id: The agent's ID
            destino: El destino al cual el carro desea llegar
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        """
        Creates a new Car agent.
        Args:
            unique_id: The agent's ID
            isInDestiny: Indica si el Carro ha lleago o no a su destino
            destino: El destino al cual el carro desea llegar
            posibleMovements: Los movimientos que un vehiculo puede hacer según su posición
        """
        self.isInDestiny = False
        self.direction = ""
        self.destino = destino
        self.posibleMovements = []

    def moveLeaveStart(self):
        """ 
        Mueve al agente fuera del destino a una casilla de tipo camino
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

    def moveToDirection(self, direction, fromPositon):
        """ 
        Regresa la posición de enfrente según la dirección hacia la cual se esta momiendo
        Tambien define los tres posibles movimientos (derecha, enfrente, izquierda) que puede hacer
        el car según su dirección. Esa misma matriz indica cuales son las direcciones a las que no
        se podría mover según determinado movimiento.
        """
        x, y = fromPositon
        if direction == "Up":
            self.posibleMovements = [((x-1,y), "Right"),((x,y+1), "Down"),((x+1,y), "Left")]
            y += 1
        elif direction == "Down":
            self.posibleMovements = [((x+1,y), "Left"),((x,y-1), "Up"),((x-1,y), "Right")]
            y -= 1
        elif direction == "Left":
            self.posibleMovements = [((x,y-1), "Up"),((x-1,y), "Right"),((x,y+1), "Down")]
            x -= 1
        elif direction == "Right":
            self.posibleMovements = [((x,y+1), "Down"),((x+1,y), "Left"),((x,y-1), "Up")]
            x += 1
        return(x, y)

    def dosyTresEnfrente(self, direction):
        """ 
        A partir de su posición actual, calcula segunda y tercera posición en frente con respecto a su dirección
        """
        x, y = self.pos
        if direction == "Up":
            dos = (x,y+2)
            tres = (x,y+3)
        elif direction == "Down":
            dos = (x,y-2)
            tres = (x,y-3)
        elif direction == "Left":
            dos = (x-2,y)
            tres = (x-3,y)
        elif direction == "Right":
            dos = (x+2,y)
            tres = (x+3,y)

        if dos[0] >= 0 and dos[0] < self.model.width and dos[1] > 0 and dos[1] < self.model.height:
            return (dos, tres)
        else:
            return False

    def calcularDistancia(self, posDestino, posAMover):
        """
        Es el calculo de una distancia dada dos posiciones
        """
        nx, ny = posDestino
        ax, ay = posAMover
        return (abs(ax - nx) + abs(ay - ny))

    def intercerciones(self):
        """ 
        Se modelan los movimientos de los agentes cuando estos se mueven entre intercecciones
        """
        if (self.pos == (1,9) or self.pos == (1,8)) and self.destino[0] > 1 and self.destino[1] < 10:
            new_position = self.posibleMovements[0][0]
        elif (self.pos == (17,11) or self.pos == (17,12)) and self.destino != (5,15) and (self.destino[0] < 14 and self.destino[1] > 12):
            new_position = self.posibleMovements[2][0]
        elif (self.pos == (7,11) or self.pos == (7,12)) and self.destino == (5,15):
            new_position = self.posibleMovements[2][0]
        elif self.pos == (13,23) and (self.destino[0] > 2 and self.destino[1] > 12 and self.destino[1] < 21):
            new_position = self.posibleMovements[0][0]
        elif (self.destino[0] > 16 and self.destino[1] < 10) and (self.pos == (13,9) or self.pos == (13,8)):
            new_position = self.posibleMovements[2][0]
        else:
            new_position = self.pos
        return new_position

    def moveIntelligent(self):
        """ 
        Momiento inteligente de los agentes. A partir de su posición acutal, los movimientos que puede hacer y su destino,
        elige cual es el movimiento que le acercará lo mas posible a su destino.
        """
        new_position = self.intercerciones()
        if new_position == self.pos:
            distancia_minima = 1000
            for pos in self.posibleMovements:
                if pos[0][0] < self.model.width and pos[0][1] < self.model.height:
                    content = self.model.grid.get_cell_list_contents([pos[0]])
                    for cell in content:
                        if (isinstance(cell, Road) and ((cell.direction != self.direction and cell.direction != pos[1]) 
                        or cell.direction == self.direction)) or isinstance(cell, Destination) and pos[0] == self.destino and not isinstance(cell, Car):
                            distancia_nueva = self.calcularDistancia(self.destino, pos[0])
                            if distancia_nueva < distancia_minima:
                                distancia_minima = distancia_nueva
                                new_position =  pos[0]
                            elif distancia_nueva == distancia_minima:
                                new_position = self.posibleMovements[1][0]
                else:
                    new_position = self.posibleMovements[1][0]

        # contentNewCell = self.model.grid.get_cell_list_contents([new_position])
        # for item in contentNewCell:
        #     if isinstance(item, Car):
        #         new_position = self.pos
        # else:
        #     new_position = new_position
        
        return new_position


    def giroValido(self, pos_move):
        """ 
        Determina si puede hacer un giro con base en si es o no un camino viable
        """
        if pos_move[0] >= 0 and pos_move[0] < self.model.width and pos_move[1] > 0 and pos_move[1] < self.model.height:
            contentCell = self.model.grid.get_cell_list_contents([pos_move])
            for item in contentCell:
                if isinstance(item, Car):
                    return False
            for item in contentCell:
                if isinstance(item, Road):
                    return True
            else:
                return False
        else: 
            return False

    def checkTrafic(self, normal_movement):
        """ 
        Observa si hay trafico (dos parados carros al frente). Si si, se mueve en una diagonal
        """
        unoEnfrente = self.posibleMovements[1][0]
        mePuedoMover = self.dosyTresEnfrente(self.direction)
        if mePuedoMover == False:
            return normal_movement
        dosEnfrente = self.dosyTresEnfrente(self.direction)[0]
        numeroCarros = 0
        contentCell = self.model.grid.get_cell_list_contents([unoEnfrente])
        for item in contentCell:
            if isinstance(item, Car):
                numeroCarros += 1
                break
        contentCell = self.model.grid.get_cell_list_contents([dosEnfrente])
        for item in contentCell:
            if isinstance(item, Car):
                numeroCarros += 1
                break
        izquierda = self.posibleMovements[0][0]
        derecha = self.posibleMovements[2][0]
        if numeroCarros != 2:
            return normal_movement
        else:
            if self.giroValido(derecha):
                self.moveToDirection(self.direction, derecha)
                if self.giroValido(self.posibleMovements[1][0]):
                    return self.posibleMovements[1][0]
                else:
                    return normal_movement
            elif self.giroValido(izquierda):
                self.moveToDirection(self.direction, izquierda)
                if self.giroValido(self.posibleMovements[1][0]):
                    return self.posibleMovements[1][0]
                else:
                    return normal_movement
            else:
                return normal_movement


    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        if self.pos == self.destino:
            new_position = self.pos
            self.isInDestiny = True

        new_position = self.pos
        currentCell = self.model.grid.get_cell_list_contents([self.pos])
        for cell in currentCell:
            if isinstance(cell, Destination) and (self.pos != self.destino):
                new_position = self.moveLeaveStart()

            elif isinstance(cell, Road):
                self.direction = cell.direction
                new_position = self.moveToDirection(self.direction, self.pos)

                # mover según lo que haya en frente
                contentCellInFront = self.model.grid.get_cell_list_contents([new_position])
                for cellFront in contentCellInFront:
                    if (self.pos == (7,15) or self.pos == (6,15)) and self.destino == (5,15):
                        new_position = (self.pos[0]-1, self.pos[1])
                    elif isinstance(cellFront, Traffic_Light):
                        if cellFront.state == False:
                            new_position = self.pos
                    elif isinstance(cellFront, Car):
                        new_position = self.pos
                    elif isinstance(cellFront, Road):
                        new_position = self.moveIntelligent()
                
                new_position = self.checkTrafic(new_position)

            elif isinstance(cell, Traffic_Light):
                new_position = self.moveToDirection(self.direction, self.pos)
                contentCellInFront = self.model.grid.get_cell_list_contents([new_position])
                for cellFront in contentCellInFront:
                    if isinstance(cellFront, Car):
                        new_position = self.pos
        
        contentNewCell = self.model.grid.get_cell_list_contents([new_position])
        for item in contentNewCell:
            if isinstance(item, Car):
                self.model.grid.move_agent(self, self.pos)
        else:
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
