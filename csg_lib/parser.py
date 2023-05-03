import math
from collections import defaultdict
import numpy as np
import torch as th
from .constants import TRANSLATE_MIN, TRANSLATE_MAX, ROTATE_MIN, ROTATE_MAX, SCALE_MIN, SCALE_MAX, ROTATE_MULTIPLIER, SCALE_ADDITION, CONVERSION_DELTA


class CSG2DParser():

    def __init__(self, device):

        self.command_n_param = {
            "ellipse": 5,
            "rectangle": 5,
            "union": 0,
            "intersection": 0,
            "difference": 0,
            "translate": 2,
            "scale": 2,
            "rotate": 1,
        }
        self.command_symbol_to_type = {
            "ellipse": "D",
            "rectangle": "D",
            "translate": "T",
            "scale": "T",
            "rotate": "T",
            "union": "B",
            "intersection": "B",
            "difference": "B",
        }
        self.transform_sequence = ["rotate", "scale", "translate"]
        self.transform_lims = {"translate": (0, 2),
                               "scale": (2, 4),
                               "rotate": (4, 5)}

        self.device = device
        self.novel_cmds = []

    def get_novel_cmds(self):
        return self.novel_cmds

    def parse(self, expression_list, use_torch=False):
        command_list = []
        draw_count = defaultdict(int)
        for ind, expr in enumerate(expression_list):
            command_symbol = expr.split("(")[0]
            if command_symbol == "$":
                # END OF EXPRESSION
                break
            else:
                command_type = self.command_symbol_to_type[command_symbol]
                command_dict = {'type': command_type, "symbol": command_symbol}
                n_param = self.command_n_param[command_symbol]
                if n_param > 0:
                    if command_type == "D":
                        command_dict["ID"] = draw_count[command_symbol]
                        draw_count[command_symbol] += 1
                    all_transforms = self.get_transforms(expr)
                    command_list.extend(all_transforms)
                command_list.append(command_dict)

        return command_list, draw_count

    def get_cmd_list(self):
        cmds = [x for x, y in self.command_n_param.items()]
        cmds += ["$"]
        return cmds

    def get_transforms(self, expr, adjust_param=True):
        param_str = expr.split("(")[1][:-1]
        param = np.array([float(x.strip())
                          for x in param_str.split(",")])
        if adjust_param:
            param[:2] *= -1
            param[2:4] = 1/(param[2:4] + CONVERSION_DELTA)
            param[4] *= math.pi / 180.
        # Now convert into MCSG3D
        all_transforms = []
        for _, command_symbol in enumerate(self.transform_sequence):
            lims = self.transform_lims[command_symbol]
            transform_dict = {
                'type': "T", "symbol": command_symbol, "param": param[lims[0]: lims[1]]}
            all_transforms.append(transform_dict)
        return all_transforms

    def set_device(self, device):
        self.device = device
