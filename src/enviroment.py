import os
import pygame
import threading
import time
from src.player import Player
from src.chessboard import Chessboard
from src.knight import Knight
from src.timer import Timer
from src.controllers.controller import Controller

class Enviroment:

    # Variables de pygame
    screen: pygame.Surface
    screen_width: int
    screen_height: int

    # Variables del entorno
    done: bool
    winner: bool
    the_winner: int
    play_number: int

    # Pantallas cuando ganan
    player1_win: pygame.image
    player2_win: pygame.image
    empate: pygame.image
    player_win: pygame.image

    # Jugadores
    player1: Player
    player2: Player

    # Turno del jugador
    player1_turn: bool

    # Constantes
    play_count: int
    PLAY_LIMIT = 100

    # Tablero de ajedrez
    chessboard: Chessboard

    # Booleana de configuracion para identificar si se grafica el tablero o no
    graph_mode: bool

    def __init__(self, screen_width: int, screen_height: int,
                       player1_command: str, player2_command: str,
                       graph_mode=True):
        self.graph_mode = graph_mode
    
        # Inicializando pygame
        pygame.init()

        if self.graph_mode:
            self.screen = pygame.display.set_mode((screen_width, screen_height))
            pygame.display.set_caption("Ajedrez")
        
        self.screen_height = screen_height
        self.screen_width = screen_width
        s_size = (screen_width, screen_height)

        # Limite de jugadas
        self.play_count = 0

        # Obtienendo directorio para la carga de recursos
        dirname = os.path.dirname(__file__)

        # Creando tablero
        path = os.path.join(dirname, "assets/Tablero.jpg")
        skin = pygame.image.load(path)
        self.chessboard = Chessboard(skin, screen_width, screen_height)

        # Cargando imagenes de victoria
        path = os.path.join(dirname, "assets/Player 1 win.png")
        self.player1_win = pygame.image.load(path)
        self.player1_win = pygame.transform.scale(self.player1_win, s_size)
        path = os.path.join(dirname, "assets/Player 2 win.png")
        self.player2_win = pygame.image.load(path)
        self.player2_win = pygame.transform.scale(self.player2_win, s_size)
        path = os.path.join(dirname, "assets/Empate.png")
        self.empate = pygame.image.load(path)
        self.empate = pygame.transform.scale(self.empate, s_size)

        # Creando jugadores
        self.player1 = Player(Player.PLAYER_ONE,
                              Controller(player1_command))
        self.player2 = Player(Player.PLAYER_TWO,
                              Controller(player2_command))
        self._add_knights()
        self.player1_turn = True

        self.done = False
        self.winner = False
        self.play_number = 0

        self.timer = Timer()

    def _add_knights(self):
        """
        Agrega los caballos iniciales a los jugadores y al tablero
        """
        # Altura y anchura de los caballos
        width = self.screen_width/8
        height = self.screen_height/8

        # Obteniendo Path de los caballos
        dirname = os.path.dirname(__file__)
        caballo_blanco = os.path.join(dirname, "assets/Caballo blanco.png")
        caballo_negro = os.path.join(dirname, "assets/Caballo negro.png")

        for player_number in [Player.PLAYER_ONE, Player.PLAYER_TWO]:
            # Obteniendo player
            player = self.player1 if player_number == Player.PLAYER_ONE \
                else self.player2

            # Cargando imagen del caballo
            file_path = caballo_blanco if player_number == Player.PLAYER_ONE \
                else caballo_negro
            skin = pygame.image.load(file_path)

            # Creando caballos del jugador
            for nc in range(16):
                id_caballo = player_number * 100 + nc

                # Calculando posicion del caballo
                x = nc % 8
                desp_y = 0 if player_number == Player.PLAYER_ONE else 6
                y = int(nc / 8) + desp_y

                # Creando caballo
                knight = Knight(x, y, skin, width, height, id_caballo)

                # Agregando caballo
                player.add_knight(knight)
                self.chessboard.add_knight(knight)

    def launch_turns(self):
        play_limit = self.PLAY_LIMIT * 2

        while not self.winner and not self.done and self.play_count < play_limit:
            self.play_count += 1

            # Obteniendo jugador en turno
            self.player1_turn = not self.player1_turn
            player = self.player1 if self.player1_turn else self.player2
            other_player = self.player1 if not self.player1_turn \
                else self.player2

            # Obteniendo accion del jugador
            state = self.chessboard.get_state(player, other_player)

            self.timer.reset()
            good_movement = False
            time_out = False
            while not good_movement:
                try:
                    action = player.get_action(state, self.timer.current_time())
                    # print("Action: ")
                    # print(action.knight_id)
                    # print(action.knight_movement)

                    # Aplicando accion
                    self.chessboard.move(player, action.knight_id, action.knight_movement)
                    good_movement = True
                except NameError as e:
                    print(f"Player {player.player_number} error: {e}")

                    # Si el controlador se demora mas de 5 segundos queda
                    # eliminado
                    if e.__str__() == "TimeOut":
                        time_out = True
                        break

                except Exception as e:
                    print("Error raro")
                    print(e)
            
            # Registrando eliminacion por time out
            if time_out or not good_movement:
                self.winner = True
                self.the_winner = other_player.player_number
                
                # Actualizando jugador ganador
                self.player_win = self.player1_win if self.the_winner == \
                    Player.PLAYER_ONE else self.player2_win

                print(f"Player {player.player_number} pierde por time out")

            # Registrando ganador
            if player.point == 16:
                self.winner = True
                self.the_winner = player.player_number
                
                # Actualizando jugador ganador
                self.player_win = self.player1_win if self.the_winner == \
                    Player.PLAYER_ONE else self.player2_win

                print(f"Player {player.player_number} win")
            # else:
            #     time.sleep(0.1)
        
        # Obteniendo ganador por limite de jugadas
        if self.play_count == play_limit:
            self.winner = True

            if self.player1.point > self.player2.point:
                self.the_winner = Player.PLAYER_ONE
                self.player_win = self.player1_win
            
            elif self.player1.point < self.player2.point:
                self.the_winner = Player.PLAYER_TWO
                self.player_win = self.player2_win
            
            else:
                self.the_winner = Player.PLAYER_PAR
                self.player_win = self.empate

    def run(self):
        """
        Comprende el ciclo del juego. Este finaliza cuando alguno de los
        jugadores gana.
        """
        t = threading.Thread(target=self.launch_turns)
        t.start()

        while not self.done and self.graph_mode:
            # Actualizando eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    continue

            player = self.player1 if self.player1_turn else self.player2
            other_player = self.player1 if not self.player1_turn \
                else self.player2

            # Limpiando ventana
            self.screen.fill((33, 33, 33))

            # Dibujando tablero y jugadores
            self.chessboard.draw(self.screen)
            other_player.draw(self.screen)
            player.draw(self.screen)

            # Dibujando timer
            self.timer.draw(self.screen)

            # Dibujando ganador de la partida
            if self.winner:
                self.screen.blit(self.player_win, (0, 0))

            # Actualizando tablero
            pygame.display.update()

        print("Esperando hilos")
        t.join()
        print("Juego finalizado")
        print("Puntaje del jugador 1: ", self.player1.point)
        print("Puntaje del jugador 2: ", self.player2.point)
