# pack_poly

CSCI 1710 project

## Project Description

Following our curiosity modeling project, we are setting out to model polymino packing. Polyminoes are generalized tetriminoes (Tetris pieces)—i.e. shapes that are formed by connecting N squares together edge to edge. The prototypical instance of a problem statement in our model is: “Given an arbitrary 2D container (a Tetris board in an arbitrary shape) and a set of polyominoes, how can I arrange the polyominoes to fill the container?” Polymino packing is an interesting and challenging problem in computational geometry and discrete mathematics, which involves solving a combinatorial optimization problem that is NP-complete. The problem is connected to various real-world applications, namely manufacturing and logistics, where efficiently packing different objects in a limited space is of relevance. This problem also offers several avenues for exploration: we can impose additional constraints such as assigning a color to each polymino, then enforcing that the packing solution does not have any of the same colors touching each other (turning it into a packing-coloring problem). We also note the existence of a “dual” problem, where we are given a container and a set of sheets of material, and the goal is to find the minimum cost cut that produces a set of polyminoes that fills the container.

## Foundation Goals

1. Create a system which can solve the packing problem for tetriminoes for arbitrary shape containers.

2. Create a system which can solve the packing problem for arbitrary order polyminoes with a fixed rectangular container.

## Target Goals

1. Map arbitrary instances of the polymino packing problem to SAT instances and solve them with appropriate packages.

2. Solve reasonably complex instances of these problems Investigate additional constraints such as polymino coloring

## Reach Goals

For our reach goals, we want to integrate the construction of polyminoes as a part of the problem statement. This system starts with a given container, and a material block. Now the system must "cut" the polyminoes from the material block as well as pack them in the container. The goal would be to maximize packing, while minimizing the number of cuts required (for example, by making many polyminoes with a single cut). Our system will output a pareto boundary of "feasible" solutions with different packing-cutting tradeoffs.
