from typing import List
from src.player import Player
from src.horse import Horse
from src.state import State
import pygame

class Chessboard:

    skin: pygame.image

    size = (8, 8)
    board: List[List[Horse]]

    def __init__(self, skin: pygame.image, width: int, height: int):
        self.board = []
        for _ in range(8):
            self.board.append([None]*8)


        # Cargando skin
        self.skin = skin
        self.skin = pygame.transform.scale(self.skin, (width, height))

    def move(self, player: Player, horse_id: int, move_id: int):
        """
        Mueve el caballo a una posicion determinada, haciendo todo lo necesario
        que implica el movimiento del caballo. Como lo es comerse a un caballo,
        denegar movimientos no validos, etc.

        Args:
            player (Player): Jugador que está realizando el movimiento.
            horse_id (int): Identificador de caballo que se esta moviendo.
            move_id (int): Identificador del movimiento del caballo.

        Raises:
            NameError: MovimientoFueraDelTablero se gatilla cuando el movimiento
                       del caballo lo lleva fuera del tablero.
            NameError: MovimientoInvalido se gatilla cuando el movimiento del
                       caballo no es valido.
        """
        # Obteniendo jugador y caballo
        horse = player.get_horse(horse_id)
        
        # ? Prueba
        x, y = horse.get_position()
        horse2 = self.board[y][x]
        x2, y2 = horse2.get_position()
        if not horse2 == horse:
            import sys
            print(f"IDS: {horse.id_} {horse2.id_}")
            print(f'POS: ({x},{y}) ({x2},{y2})')
            print("Error, son distintos")
            self.print_board()
            #sys.exit()

        if not horse.alive:
            raise NameError("CaballoMuerto")

        # Obtieniendo posiciones del caballo
        x, y = horse.get_position()
        nx, ny = horse.get_movement(move_id)
        
        if ny < 0 or ny >= len(self.board) or nx < 0 or nx >= len(self.board[ny]):
            raise NameError("MovimientoFueraDelTablero")

        other_horse = self.board[ny][nx]
        if other_horse is None:
            self.board[y][x] = None
            self.board[ny][nx] = horse
            horse.set_position(nx, ny)
        elif player.is_enemy(other_horse):
            player.add_point()
            self.board[y][x] = None
            self.board[ny][nx] = horse
            horse.set_position(nx, ny)
            other_horse.alive = False
        else: 
            # Este error se gatilla cuando se intenta ir a una casilla con un
            # aleado en ella.
            raise NameError("MovimientoInvalido")

    def add_horse(self, horse: Horse):
        """
        Agrega un nuevo caballo al tablro

        Args:
            horse (Horse): El nuevo caballo que se quiere agregar al tablero
        """
        x = horse.x
        y = horse.y

        self.board[y][x] = horse

    def get_state(self, player: Player, enemy_player: Player) -> State:
        """
        Obtiene el estado actual del programa

        Returns:
            State: Estado actual del programa
        """
        
        ids = []
        for _ in range(8):
            ids.append([None]*8)

        my_horses = []
        for _ in range(8):
            my_horses.append([None]*8)

        enemy_horses = []
        for _ in range(8):
            enemy_horses.append([None]*8)
        
        my_horses_dict = {}
        enemy_horses_dict = {}


        # Cargando estado
        for id_horse, horse in player.horses.items():
            if not horse.alive:
                continue
            ids[horse.y][horse.x] = id_horse
            my_horses[horse.y][horse.x] = id_horse
            my_horses_dict[id_horse] = (horse.x, horse.y)

        for id_horse, horse in enemy_player.horses.items():
            if not horse.alive:
                continue
            ids[horse.y][horse.x] = id_horse
            enemy_horses[horse.y][horse.x] = id_horse
            enemy_horses_dict[id_horse] = (horse.x, horse.y)

        # Creando y retornando el estado
        return State(ids, my_horses, my_horses_dict,
                     enemy_horses, enemy_horses_dict)

    def draw(self, screen: pygame.surface.Surface):
        """
        Dibuja el tablero en la ventana

        Args:
            screen (pygame.surface.Surface): Superficie donde se va a dibujar
                                             el tablero.
        """
        screen.blit(self.skin, (0, 0))

    def print_board(self):
        for linea in self.board:
            for horse in linea:
                if horse is None:
                    print("None", end=" ")
                else:
                    print(horse.id_, end=" ")
            print()