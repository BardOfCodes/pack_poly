from .parser import CSG2DParser
from .compiler import CSG2DCompiler
from collections import defaultdict
import numpy as np
import torch as th


class CSG2DExecutor:

    def __init__(self, resolution, device):

        self.resolution = resolution
        self.device = device
        self.parser = CSG2DParser(device)
        self.compiler = CSG2DCompiler(resolution, device)

    def execute(self, expression):

        parsed_graphs, draw_count = self.parser.parse(expression)

        draw_transforms, inversion_array, intersection_matrix = self.compiler.fast_compile(
            parsed_graphs, draw_count)
        inversion_array = inversion_array.to(self.device)
        intersection_matrix = intersection_matrix.to(self.device)
        canvas = self.compiler.evaluate(
            draw_transforms, inversion_array, intersection_matrix)

        canvas = canvas.reshape(self.resolution, self.resolution)
        canvas = (canvas <= 0).float()

        return canvas

    def compile(self, expression):
        parsed_graphs, draw_count = self.parser.parse(expression)
        draw_transforms, inversion_array, intersection_matrix = self.compiler.fast_sub_compile(
            parsed_graphs, draw_count)
        return draw_transforms, inversion_array, intersection_matrix

    def eval_batch_execute(self, expression_batch):

        cache = []

        for _, expression in enumerate(expression_batch):
            expr_obj = self.compile(expression)
            cache.append(expr_obj)

        collapsed_draws = defaultdict(list)
        collapsed_inversions = defaultdict(list)
        all_draws = []
        all_graphs = []

        for val in cache:

            draw_transforms, draw_inversions, graph = val

            all_draws.append(draw_transforms)
            all_graphs.append(graph)
            for draw_type, transforms in draw_transforms.items():
                collapsed_draws[draw_type].extend(transforms)
                collapsed_inversions[draw_type].extend(
                    draw_inversions[draw_type])

        for draw_type in draw_transforms.keys():
            if len(collapsed_draws[draw_type]) == 0:
                continue
            collapsed_inversions[draw_type] = th.from_numpy(
                np.array(collapsed_inversions[draw_type])).to(self.compiler.device)
            collapsed_inversions[draw_type] = collapsed_inversions[draw_type].unsqueeze(
                1)
            collapsed_draws[draw_type] = th.stack(
                collapsed_draws[draw_type], 0).to(self.compiler.device)
        canvas = self.compiler.batch_evaluate_with_graph(collapsed_draws, all_draws,
                                                         collapsed_inversions,
                                                         all_graphs)

        canvas = canvas.reshape(-1, self.resolution, self.resolution)
        canvas = (canvas <= 0).float()

        return canvas
