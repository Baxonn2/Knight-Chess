from typing import List, Dict, Tuple

class State:

    ids: List[List[int]]
    enemy_knights: List[List[int]]
    enemy_knights_dict: Dict[int, Tuple[int, int]]
    my_knights: List[List[int]]
    my_knights_dict: Dict[int, Tuple[int, int]]
    time_less: float

    def __init__(self, ids, my_knights, my_knights_dict,
                enemy_knights, enemy_knights_dict):
        self.ids = ids
        self.enemy_knights = enemy_knights
        self.enemy_knights_dict = enemy_knights_dict
        self.my_knights = my_knights
        self.my_knights_dict = my_knights_dict
        self.time_less = 0

    def set_time_less(self, seconds: float):
        self.time_less = seconds
