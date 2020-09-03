class Action:

    horse_id: int       # Identificador del caballo
    horse_movement: int # Movimiento del caballo

    # Los movimientos de un caballo C están definidos por:
    #   + 7 + 0 +
    #   6 + + + 1
    #   + + C + +
    #   5 + + + 2
    #   + 4 + 3 +

    def __init__(self, horse_id: int, horse_movement: int):
        self.horse_id = horse_id
        self.horse_movement = horse_movement