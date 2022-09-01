import json
import numpy as np
from pydantic import BaseModel
from pydantic import parse_obj_as

vic_duty_values = [
    [0, 0.00, 0],
    [125_000, 0.02, 350],
    [250_000, 0.050, 2870],
    [925_000, 0.10, 18_370],
    [1500_000, 0.12, 28_070], # 52_800 is 960_000 * 0.055
    [10_000_000_000, 0.0, 0]
]

def duty_calculator(value):
    current_stamp_duty = 0
    for i, v in enumerate(vic_duty_values):
        if value > v[0]:
            
            next_list = vic_duty_values[i + 1]
            high_val = next_list[0]
            if value<high_val:
                high_val = value
            current_stamp_duty = current_stamp_duty + ((high_val - v[0])*v[1])
    return current_stamp_duty