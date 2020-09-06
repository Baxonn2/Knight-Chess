class Action:

    knight_id: int       # Identificador del caballo
    knight_movement: int # Movimiento del caballo

    # Los movimientos de un caballo C están definidos por:
    #   + 7 + 0 +
    #   6 + + + 1
    #   + + C + +
    #   5 + + + 2
    #   + 4 + 3 +

    def __init__(self, knight_id: int, knight_movement: int):
        self.knight_id = knight_id
        self.knight_movement = knight_movement