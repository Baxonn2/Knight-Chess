from src.enviroment import Enviroment
import sys

if __name__ == "__main__":
    # Obteniendo el controlador del segundo player
    try:
        player2_command = sys.argv[2]
    except IndexError as e:
        print("Player 2 en forma aleatoria")
        player2_command = "python3 random_controller.py"

    # Obteniendo el controlador del primer player
    try:
        player1_command = sys.argv[1]
    except IndexError as e:
        print("Player 1 en forma aleatoria")
        player1_command = "python3 random_controller.py"
    
    env = Enviroment(400, 400, player1_command, player2_command)
    env.run()
