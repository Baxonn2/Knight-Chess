import datetime
import pygame

class Timer:

    init_time: datetime.datetime
    limit_time: datetime.datetime
    font: pygame.font.Font
    
    # Tiempo limite para realizar una accion
    TIME_OUT = datetime.timedelta(seconds=5)

    def __init__(self):
        self.reset()
    
    def reset(self):
        self.font = pygame.font.Font(None, 20)
        self.init_time = datetime.datetime.now()
        self.limit_time = self.init_time + self.TIME_OUT

    def current_time(self) -> datetime.timedelta:
        """
        Obtiene el tiempo transcurrido desde que se inicializó el timer

        Returns:
            datetime.timedelta: Tiemop transcurrido desde que se inicilizó el
                                timer.
        """
        if self.time_out():
            return datetime.timedelta(seconds=0)
        return self.limit_time - datetime.datetime.now()

    def time_out(self) -> bool:
        return datetime.datetime.now() > self.limit_time

    def draw(self, screen: pygame.surface.Surface):
        current_time = self.current_time()
        seconds = current_time.seconds
        miliseconds = int(current_time.microseconds/10000)
        rojo = 255 - 255 * (seconds/self.TIME_OUT.seconds)
        text = self.font.render(f'{seconds}:{miliseconds}', True, (rojo, 128, 0))
        screen.blit(text, (0, 0))