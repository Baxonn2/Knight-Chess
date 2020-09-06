from typing import List, Dict, Tuple

class State:

    ids: List[List[int]]
    enemy_horses: List[List[int]]
    enemy_horses_dict: Dict[int, Tuple[int, int]]
    my_horses: List[List[int]]
    my_horses_dict: Dict[int, Tuple[int, int]]
    time_less: float

    def __init__(self, ids, my_horses, my_horses_dict,
                enemy_horses, enemy_horses_dict):
        self.ids = ids
        self.enemy_horses = enemy_horses
        self.enemy_horses_dict = enemy_horses_dict
        self.my_horses = my_horses
        self.my_horses_dict = my_horses_dict
        self.time_less = 0

    def set_time_less(self, seconds: float):
        self.time_less = seconds
