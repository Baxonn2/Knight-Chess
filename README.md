# Knight-Chess
Juego de tablero de ajedrez de caballos diseñador principalmente para formar parte de un entorno competitivo de algoritmos de juegos.

## Dependencias
Para poder ejecutar este programa es necesario python 3 y una liberia llamda pygame. Para instalar esta última basta con utilizar
```
pip3 install pygame
```  
Si estás utilizando MacOS y al ejecutar el programa sale una ventana en negro (o el blanco) y no se muestra el tablero es probable que necesites desinstalar e instalar pygame utilizando el siguiente comando `python3 -m pip install pygame==2.0.0.dev6`.

## Ejecución
Para ejecutar el programa basta con ejecutar el main.py con el comando `python3 main.py`. Esto cargará el programa con un controlador "random" para ambos jugadores. Sin embargo en caso de querer modificar el controlador con el que se va a ejecutar el programa se puede hacer lo siguiente: 
```bash
python3 main.py "{comando1}" "{comando2}"
```
Esto especifica el comando a utilizar para llamar a un controlador del programa. En la parte de "Especificar controlador" hay mas detalles sobre esto.

## Controladores
Los controladores son los que le dan la inteligencia a los jugadores.  
El juego por defecto contiene un controlador que selecciona un caballo aleado y le asigna un movimiento aleatorio. Éste se llama random_controller.py y se encuentra en la raíz del programa. Es importante señalar que este es el controlador que se llama por defecto si es que no se le ha asignado un controlador especifico para un jugador.  

### Especificar controlador
Para especificar el controlador que se va a utilizar por un jugador se debe correr este programa de la siguiente manera:
```bash
python3 main.py "comando1" "comando2"
```
Donde `"comando1"` es el comando que se va a utilizar para llamar al programa controlador del primer jugador y el `"comando2"` es el comando que se va a utilizar para llamar al programa controlador del segundo jugador. En caso de que no se especifique el segundo comando, el programa asumirá que el segundo controlador es el random_controller.py que se mencionó anteriormente.  
Un ejemplo para que quede mas claro:
```bash
python3 main.py "python3 my_controller.py"
```
Esta forma de ejecutar el main.py definiría un controlador para el jugador 1. Este controlador sería un código escrito en python llamado my_controller.py ubicado en la raiz de este programa. Además, en este caso, como no se especifica el controlador para el jugador 2, se utilizaría el controlador random_controller.py.

### Entradas de un controlador

Los controladores reciben como parametro una cadena de texto en formato json. Un ejemplo del contenido de este json sería el siguiente:

```json
{
    "ids": [[100, 101, 102, 103, 104, 105, 106, 107], [108, 109, 110, 111, 112, 113, 114, 115], [null, null, null, null, null, null, null, null], [null, null, null, null, null, null, null, null], [null, null, null, null, null, null, null, null], [null, null, null, null, null, null, null, 214], [200, 201, 202, 203, 204, 205, 206, 207], [208, 209, 210, 211, 212, 213, null, 215]], 
    "enemy_horses": [[null, null, null, null, null, null, null, null], [null, null, null, null, null, null, null, null], [null, null, null, null, null, null, null, null], [null, null, null, null, null, null, null, null], [null, null, null, null, null, null, null, null], [null, null, null, null, null, null, null, 214], [200, 201, 202, 203, 204, 205, 206, 207], [208, 209, 210, 211, 212, 213, null, 215]], 
    "enemy_horses_dict": {"200": [0, 6], "201": [1, 6], "202": [2, 6], "203": [3, 6], "204": [4, 6], "205": [5, 6], "206": [6, 6], "207": [7, 6], "208": [0, 7], "209": [1, 7], "210": [2, 7], "211": [3, 7], "212": [4, 7], "213": [5, 7], "214": [7, 5], "215": [7, 7]}, 
    "my_horses": [[100, 101, 102, 103, 104, 105, 106, 107], [108, 109, 110, 111, 112, 113, 114, 115], [null, null, null, null, null, null, null, null], [null, null, null, null, null, null, null, null], [null, null, null, null, null, null, null, null], [null, null, null, null, null, null, null, null], [null, null, null, null, null, null, null, null], [null, null, null, null, null, null, null, null]], 
    "my_horses_dict": {"100": [0, 0], "101": [1, 0], "102": [2, 0], "103": [3, 0], "104": [4, 0], "105": [5, 0], "106": [6, 0], "107": [7, 0], "108": [0, 1], "109": [1, 1], "110": [2, 1], "111": [3, 1], "112": [4, 1], "113": [5, 1], "114": [6, 1], "115": [7, 1]}
}
```
* **ids**: Es matríz correspondiente al estado actual del tablero. Los valores corresponden a los identificadores de los caballos
* **enemy_horses**: Es una matriz que corresponde al estado actual del tablero. Muy similar *ids* pero solo contiene los caballos enemigos.
* **my_horses**: Igual que el anterior pero solo contiene caballos aleados.
* **enemy_horses_dict**: Corresponde a un diccionario de caballos enemgios donde las "llaves" indican el identificador del caballo y el valor un par numérico correspondientes a las coordenadas actual de dicho animal.
* **my_horses_dict**: Diccionario igual que el anterior pero con caballos aliados.

### Salidas del controlador
Las salidas del controlador no son mas que una salida por consola (un print, printf, std::out, system.out.println, echo, etc.) que contiene un formato json con el identificador del caballo a mover (horse_id) y el identificador del movimiento a hacer (horse_movement). En otras palabras, el controlador debe imprimir por consola algo como esto:
```json
{
    "horse_id": "112",
    "horse_movement": 6
}
```
Notar que el valor de horse_movement va de 0 a 7. Estos valores corresponden a los siguientes movimientos (C es el caballo):
```
     + 7 + 0 +
     6 + + + 1
     + + C + +
     5 + + + 2
     + 4 + 3 +
```
Un ejemplo de código de un controlador es el siguiente (en python):
```python
import random   # Libreria para hacer cosas aleatorias
import json     # Libreria para manipular cadenas en formato json
import sys      # Libreria para los argumentos del programa

if __name__ == "__main__":
    # Obteniendo cadena de entrada (formato json)
    state_json = sys.argv[1]

    # Transformando la cadena de entrada en diccionario
    state = json.loads(state_json) 

    # Obteniendo lista de caballos
    my_horses = list(state['my_horses_dict'].keys())
    
    # Eligiendo caballo aleatoriamente
    horse_id = random.choice(my_horses)

    # Eligiendo movimiento aleatoriamente
    horse_movement = random.choice(range(7))

    # Creando diccionario de resultado
    result = {
        "horse_id": horse_id,
        "horse_movement": horse_movement
    }

    # Imprimiendo resultado
    print(json.dumps(result))
```
Este ejemplo es en verdad el controlador random_controller.py.

