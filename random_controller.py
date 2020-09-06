import random
import json
import sys
from time import sleep

if __name__ == "__main__":
    state_json = sys.argv[1]

    # Cambiando caracter raro de comillas por doble comillas
    #! Probar si esto funciona en todos los SO
    state_json = state_json.replace(r'\"', '"')

    state = json.loads(state_json)

    my_horses = list(state['my_horses_dict'].keys())
    
    # Creando diccionario de resultado
    result = {
        "horse_id": random.choice(my_horses),
        "horse_movement": random.choice(range(7))
    }

    # Imprimiendo resultado
    #! Puede que la entrega del resultado tambien tenga que se procesada de la
    #! misma forma que la entrda
    print(json.dumps(result))
