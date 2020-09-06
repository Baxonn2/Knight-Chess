from src.state import State
from src.action import Action
import os
import json
import threading
import datetime

class Controller:

    command_init: str
    command_end: str
    command: str
    result: str

    def __init__(self, command_init: str, command_end=""):
        self.command_init = command_init
        self.command_end = command_end
        self.command = ""
        self.result = ""

    def get_result(self):
        self.result = os.popen(self.command).read()

    def get_action(self, state: State, time_less: datetime.timedelta) -> Action:
        # Actualizando tiempo limite
        time_out = time_less.seconds + time_less.microseconds/1000000.0
        state.set_time_less(seconds=time_out)

        my_json = json.dumps(state.__dict__)
        my_json = my_json.translate(str.maketrans({'"': r'\"'}))
        self.command = f'{self.command_init} "{my_json}" {self.command_end}'
        
        # El resultado tiene que ser un print de un json
        # print(f"Ejecutando comando {self.command}")
        
        # Obteniendo el resultado con tiempo limite de 5 segundos
        self.result = None
        t = threading.Thread(target=self.get_result)
        t.start()
        # print("Tiempo limite para el hilo:", time_out)
        
        t.join(timeout=time_out)

        # Si no se obtuvo el resultado en 5 segundos salta un error
        if self.result is None:
            raise NameError("TimeOut")
        
        # Imprimiendo el resultado obtenido
        # print(f'Resultado obtenido {self.result}\n\n')

        result_json = json.loads(self.result)

        return Action(horse_id=int(result_json['horse_id']),
                      horse_movement=int(result_json['horse_movement']))