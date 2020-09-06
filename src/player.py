from typing import Dict
from src.knight import Knight
from src.state import State
from src.action import Action
from src.controllers.controller import Controller
import pygame
import datetime

class Player:

    # Variables de estados del jugador
    knights: Dict[int, Knight]        # Diccionario de caballos aliados
    point: int                      # Cantidad de caballos comidos

    # Identificadores del player
    PLAYER_ONE = 1
    PLAYER_TWO = 2
    player_number: int

    controller: Controller

    def __init__(self, player_number: int, controller: Controller):
        self.knights = {}
        self.point = 0
        self.player_number = player_number
        self.controller = controller

    def add_knight(self, knight: Knight):
        """
        Agrega un nuevo caballo al jugador

        Args:
            knight (Knight): Caballo que se quiere agregar al jugador
        """
        self.knights[knight.id_] = knight

    def get_knight(self, knight_id: int) -> Knight:
        """
        Obtiene un caballo dada un identificador

        Args:
            knight_id (int): Identificador del caballo que se quiere obtener

        Returns:
            Knight: Retorna el caballo si es que se encuentra y None en caso de
                   que no exista dicho caballo.
        """
        return self.knights[knight_id]

    def is_enemy(self, knight: Knight) -> bool:
        """
        Comprueba si el caballo ingresado como parametro es un enemigo o no.

        Args:
            self (knight): Caballo que podria o no ser enemigo

        Returns:
            bool: Retorna True si es un caballo enemigo y False si es aliado.
        """
        return knight.id_ not in self.knights

    def add_point(self):
        """
        Agrega un punto al jugador
        """
        self.point += 1

    def draw(self, screen: pygame.surface.Surface):
        """
        Dibuja los caballos del jugador en pantalla

        Args:
            screen (pygame.surface.Surface): Superficie donde se van a dibujar
                                             los caballos.
        """
        for knight in self.knights.values():
            if knight.alive:
                knight.draw(screen)

    def get_action(self, state: State, time_less: datetime.timedelta) -> Action:
        """
        Obtiene una accion usando el controlador inicializado en el constructor
        del player

        Args:
            state (State): Estado actual del problema

        Returns:
            Action: Accion que se va a aplicar
        """
        return self.controller.get_action(state, time_less)