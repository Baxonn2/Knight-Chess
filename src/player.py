from typing import Dict
from src.horse import Horse
from src.state import State
from src.action import Action
from src.controllers.controller import Controller
import pygame
import datetime

class Player:

    # Variables de estados del jugador
    horses: Dict[int, Horse]        # Diccionario de caballos aliados
    point: int                      # Cantidad de caballos comidos

    # Identificadores del player
    PLAYER_ONE = 1
    PLAYER_TWO = 2
    player_number: int

    controller: Controller

    def __init__(self, player_number: int, controller: Controller):
        self.horses = {}
        self.point = 0
        self.player_number = player_number
        self.controller = controller

    def add_horse(self, horse: Horse):
        """
        Agrega un nuevo caballo al jugador

        Args:
            horse (Horse): Caballo que se quiere agregar al jugador
        """
        self.horses[horse.id_] = horse

    def get_horse(self, horse_id: int) -> Horse:
        """
        Obtiene un caballo dada un identificador

        Args:
            horse_id (int): Identificador del caballo que se quiere obtener

        Returns:
            Horse: Retorna el caballo si es que se encuentra y None en caso de
                   que no exista dicho caballo.
        """
        return self.horses[horse_id]

    def is_enemy(self, horse: Horse) -> bool:
        """
        Comprueba si el caballo ingresado como parametro es un enemigo o no.

        Args:
            self (horse): Caballo que podria o no ser enemigo

        Returns:
            bool: Retorna True si es un caballo enemigo y False si es aliado.
        """
        return horse.id_ not in self.horses

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
        for horse in self.horses.values():
            if horse.alive:
                horse.draw(screen)

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