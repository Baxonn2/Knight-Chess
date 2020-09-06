from typing import Tuple
import pygame

class Horse:

    x: int                      # Posicion en el eje X del caballo
    y: int                      # Posicion en el eje Y del caballo
    width: int                  # Anchura de la apariencia del caballo
    height: int                 # Altura de la apariencia del caballo
    skin: pygame.image          # Apariencia del caballo
    id_: int                    # Identificador del caballo
    alive: bool                 # Identifica si el caballo está vivo

    real_x: float
    real_y: float

    def __init__(self, x: int, y: int, skin: pygame.image, width: int,
                 height: int, id_: int):
        self.x = x
        self.y = y
        self.skin = skin
        self.width = int(width)
        self.height = int(height)
        self.id_ = id_

        self.alive = True
        self.real_x = 0
        self.real_y = 0

        # Reescalando skin
        self.skin = pygame.transform.scale(self.skin, (self.width, self.height))

    def draw(self, surface: pygame.Surface):
        """
        Dibuja el caballo en pantalla

        Args:
            surface (pygame.Surface): Superficie donde se va a dibujar el
                                      caballo.
        """
        # Actualizando posicion real
        objetive_x = self.x * self.width
        objetive_y = self.y * self.height
        self.real_x = self.real_x + (objetive_x - self.real_x) / 5
        self.real_y = self.real_y + (objetive_y - self.real_y) / 5

        actual_pos = (self.real_x + self.width/2, self.real_y + self.height/2)
        objetive_pos = (int(objetive_x + self.width/2), int(objetive_y + self.height/2))

        pygame.draw.line(surface, (255, 0, 0), actual_pos, objetive_pos, 2)
        pygame.draw.circle(surface, (255,0,0), objetive_pos, 3)
        surface.blit(self.skin, (self.real_x, self.real_y))

    def get_position(self) -> Tuple[int, int]:
        """
        Obtiene la posicion actual del caballo en el tablero

        Returns:
            Tuple[int, int]: Tupla de coordenadas de la posicion del caballo en
                             el tablero.
        """
        return self.x, self.y

    def set_position(self, x: int, y: int):
        """
        Establece una nueva posicion del caballo en el tablero.

        Args:
            x (int): Posicion en el eje X del caballo en el tablero.
            y (int): Posicion en el eje Y del caballo en el tablero.
        """
        self.x = x
        self.y = y

    def get_movement(self, movement_number: int) -> Tuple[int, int]:
        """
        Obtiene las coordenadas del caballo si se aplicara un movimiento pre-
        definido. La numeración de los movimientos es la siguiente:
                                    + 4 + 3 +
                                    5 + + + 2
                                    + + C + +
                                    6 + + + 1
                                    + 7 + 0 +

        Args:
            movement_number (int): Numero del movimiento a realizar

        Returns:
            Tuple[int, int]: Tupla de coordenadas de la posicion del caballo en
                             el tablero si se aplicara el movimiento indicado.
        """
        nx = self.x
        ny = self.y
        if movement_number == 0:
            nx += 1
            ny += 2
        elif movement_number == 1:
            nx += 2
            ny += 1
        elif movement_number == 2:
            nx += 2
            ny += -1
        elif movement_number == 3:
            nx += 1
            ny += -2
        elif movement_number == 4:
            nx += -1
            ny += -2
        elif movement_number == 5:
            nx += -2
            ny += -1
        elif movement_number == 6:
            nx += -2
            ny += 1
        elif movement_number == 7:
            nx += -1
            ny += 2
        else:
            print("Error: Movimiento no encontrado")
        return nx, ny
