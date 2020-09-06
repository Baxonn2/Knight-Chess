from src.state import State
from src.action import Action
import os
import json

class Controller:

    command_init: str
    command_end: str

    def __init__(self, command_init: str, command_end=""):
        self.command_init = command_init
        self.command_end = command_end

    def get_action(self, state: State) -> Action:
        my_json = json.dumps(state.__dict__)
        my_json = my_json.translate(str.maketrans({'"': r'\"'}))
        command = f"{self.command_init} '{my_json}' {self.command_end}"
        
        # El resultado tiene que ser un print de un json
        print(f"Ejecutando comando {command}")
        result = os.popen(command).read()
        print(f'Resultado obtenido {result}\n\n')

        result_json = json.loads(result)

        return Action(horse_id=int(result_json['horse_id']),
                      horse_movement=int(result_json['horse_movement']))