from typing import List
from src.player import Player
from src.knight import Knight
from src.state import State
import pygame

class Chessboard:

    skin: pygame.image

    size = (8, 8)
    board: List[List[Knight]]

    def __init__(self, skin: pygame.image, width: int, height: int):
        self.board = []
        for _ in range(8):
            self.board.append([None]*8)


        # Cargando skin
        self.skin = skin
        self.skin = pygame.transform.scale(self.skin, (width, height))

    def move(self, player: Player, knight_id: int, move_id: int):
        """
        Mueve el caballo a una posicion determinada, haciendo todo lo necesario
        que implica el movimiento del caballo. Como lo es comerse a un caballo,
        denegar movimientos no validos, etc.

        Args:
            player (Player): Jugador que está realizando el movimiento.
            knight_id (int): Identificador de caballo que se esta moviendo.
            move_id (int): Identificador del movimiento del caballo.

        Raises:
            NameError: MovimientoFueraDelTablero se gatilla cuando el movimiento
                       del caballo lo lleva fuera del tablero.
            NameError: MovimientoInvalido se gatilla cuando el movimiento del
                       caballo no es valido.
        """
        # Obteniendo jugador y caballo
        knight = player.get_knight(knight_id)
        
        # ? Prueba
        x, y = knight.get_position()
        knight2 = self.board[y][x]
        x2, y2 = knight2.get_position()
        if not knight2 == knight:
            import sys
            print(f"IDS: {knight.id_} {knight2.id_}")
            print(f'POS: ({x},{y}) ({x2},{y2})')
            print("Error, son distintos")
            self.print_board()
            #sys.exit()

        if not knight.alive:
            raise NameError("CaballoMuerto")

        # Obtieniendo posiciones del caballo
        x, y = knight.get_position()
        nx, ny = knight.get_movement(move_id)
        
        if ny < 0 or ny >= len(self.board) or nx < 0 or nx >= len(self.board[ny]):
            raise NameError("MovimientoFueraDelTablero")

        other_knight = self.board[ny][nx]
        if other_knight is None:
            self.board[y][x] = None
            self.board[ny][nx] = knight
            knight.set_position(nx, ny)
        elif player.is_enemy(other_knight):
            player.add_point()
            self.board[y][x] = None
            self.board[ny][nx] = knight
            knight.set_position(nx, ny)
            other_knight.alive = False
        else: 
            # Este error se gatilla cuando se intenta ir a una casilla con un
            # aleado en ella.
            raise NameError("MovimientoInvalido")

    def add_knight(self, knight: Knight):
        """
        Agrega un nuevo caballo al tablro

        Args:
            knight (Knight): El nuevo caballo que se quiere agregar al tablero
        """
        x = knight.x
        y = knight.y

        self.board[y][x] = knight

    def get_state(self, player: Player, enemy_player: Player) -> State:
        """
        Obtiene el estado actual del programa

        Returns:
            State: Estado actual del programa
        """
        
        ids = []
        for _ in range(8):
            ids.append([None]*8)

        my_knights = []
        for _ in range(8):
            my_knights.append([None]*8)

        enemy_knights = []
        for _ in range(8):
            enemy_knights.append([None]*8)
        
        my_knights_dict = {}
        enemy_knights_dict = {}


        # Cargando estado
        for id_knight, knight in player.knights.items():
            if not knight.alive:
                continue
            ids[knight.y][knight.x] = id_knight
            my_knights[knight.y][knight.x] = id_knight
            my_knights_dict[id_knight] = (knight.x, knight.y)

        for id_knight, knight in enemy_player.knights.items():
            if not knight.alive:
                continue
            ids[knight.y][knight.x] = id_knight
            enemy_knights[knight.y][knight.x] = id_knight
            enemy_knights_dict[id_knight] = (knight.x, knight.y)

        # Creando y retornando el estado
        return State(ids, my_knights, my_knights_dict,
                     enemy_knights, enemy_knights_dict)

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
            for knight in linea:
                if knight is None:
                    print("None", end=" ")
                else:
                    print(knight.id_, end=" ")
            print()