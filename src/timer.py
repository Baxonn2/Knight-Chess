import datetime
import pygame

class Timer:

    init_time: datetime.datetime
    font: pygame.font.Font

    def __init__(self):
        self.font = pygame.font.Font(None, 20)
        self.init_time = datetime.datetime.now()
    
    def current_time(self) -> datetime.timedelta:
        """
        Obtiene el tiempo transcurrido desde que se inicializó el timer

        Returns:
            datetime.timedelta: Tiemop transcurrido desde que se inicilizó el
                                timer.
        """
        return datetime.datetime.now() - self.init_time

    def draw(self, screen: pygame.surface.Surface):
        current_time = self.current_time()
        seconds = current_time.seconds
        miliseconds = int(current_time.microseconds/10000)
        text = self.font.render(f'{seconds}:{miliseconds}', True, (0, 128, 0))
        screen.blit(text, (0, 0))