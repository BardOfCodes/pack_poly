![banner](./figures/banner.jpg)

# pack_poly

CSCI 1710 Project - Polyomino Packing (in Z3)

Group: Aditya Ganeshan, Arman Maesumi

Instructions for running the code can be found in [./instructions.md](./instructions.md)

## Model Overview

Before creating Z3 constraints, we first needed to decide on a polyomino representation (i.e. how we represent a single polyomino). We chose to canonicalize the polyominoes (keeping one tile at the origin (0,0)), then represent the piece structure using integer offsets from the origin, i.e. (+1, -2). Rotation flags for angles 0, 90, 180, 270 degrees are represented using a BitVec of size 2. Additionally, we represent the container as a 2D array of boolean values. Note, we do not allow reflections in the pieces!

Our Z3 model uses these representations to enforce the following constraints;
for all polyominoes with respect to their locations and rotations, we ensure they are:
1. Placed inside container
2. Non-overlapping
3. Not placed on blocked cell

We also optionally experiment with two other constraints A) requires that all board tiles are filled B) requires that all polyominoes have been placed. These constraints are useful for different packing tasks. For instance, "A" is useful for exact cover tasks; whereas if you have a surplus of polyominoes (all polyominoes cannot fit in the container), then you would disable "B".

![packing8x8](./figures/packing8x8.png)
Figure 1. An example instance of an 8x8 board with four (white tiles) that are "blocked." We pack the container using the set of canonical pentaminoes.

We define the Z3 model and solving routine in `./packing/packing.py`

## Verification / Property-based Testing

In order to test the validity of our model, we procedurally produce random packing configurations using 2D CSG programs. The procedural algorithm greedily places (with rejection) random polyominoes on a discrete canvas. The process terminates after too many rejections or a fixed number of placements occur.

By construction, these procedurally generated polyomino configurations are guaranteed to have a solution, so we check validity simply by running our model on these configurations.

All procedural generation code is located in `./generator/`

## Investigation of Packing Stability

We investigated the notion of "stability" in polyomino packing configurations. For a given configuration (a set of polyominoes and a fixed container), we measure stability by asking: "if we introduce noise to the set of polyominoes, does the configuration remain packable?" More concretely, for the given set of polyominoes, we measure the probability that the configuration remains packable after a single piece has been randomly swapped out for another piece. We hope to discover polyomino sets that are more robust against noisey perturbation. This problem is motivated in our presentation, we spare those details in this write-up.

We first compute packings (if they exist) for all combinations with replacement of the given set of polyominoes with respect to a fixed container. We then compute stability scores for each combination by enumerating its neighboring combinations (polyomino sets with distance `K` from the original set).

![stability](./figures/stability1.gif)
Figure 2. This GIF demonstrates a given polyomino set that is particularly stable: it is packable even with small perturbations in the available pieces. This configuration was identified by our model.

The code for computing stability can be found in `./stability.py`. The computation of packings over all combinations was done in parallel on the CCV Oscar cluster using 32 cores.

### Hypothesis testing regarding stability

One question we asked was, how does stability change as `K` increases? `K` corresponds to the amount of noise introduced to the original polyomino configuration, we hypothesized that stability should decrease as `K` increases. We found a counter example to this hypothesis using Z3; however, it seems that this property *usually* holds, but not always. Details are presented in the final presentation, we share a result of this hypothesis here:

![stability_hypothesis](./figures/stability_hypothesis.jpg)
Figure 3. This packing was found as a counter example to our hypothesis. The above configuration has the following stability: Stability(K=1): 0.583, Stability(K=2): 0.868, Stability(K=3): 0.734, Stability(K=4): 0.490. We see that `K=2` offers higher stability than, say, `K=1`.

![stability_plot](./figures/stability_plot.png)
Figure 4. We see that our hypothesis is true in the *average* case. We plot the average stability values over all combinations for varying values of `K`.

## Q/A:

1. **What tradeoffs did you make in choosing your representation? What else did you try that didn’t work as well?** We chose to omit "reflection" as a possible operation available to the packer partially due to complexity of the SMT problem. Our packing problems were already quite complex (in terms of state-space). Also, we found that converting our `rotation` flags to a `BitVec` type, rather than `int` helped quite a bit.

2. **What assumptions did you make about scope? What are the limits of your model?** The model is most limited by scale of the packing problem (of course). We found that, even for relatively small configurations, Z3 needed to run for several hours. For instance, `Figure 1` took about 7 hours to complete. This limited our scope in scale (size of polyominoes and board, and number of polyominoes).

3. **Did your goals change at all from your proposal? Did you realize anything you planned was unrealistic, or that anything you thought was unrealistic was doable?** Our stretch goals did change, but not due to them being unrealistic. Originally we proposed investigated polyomino packing with the added constraint that neighboring pieces should not have the same color (i.e. graph coloring + polyomino packing). We chose to pursue the "stable packing" route instead because it appeared as a more intellectually interesting question; additionally, the graph coloring seemed like a trivial addon to the model.

4. **How should we understand an instance of your model and what your custom visualization shows?** This is addressed in the above figure captions.

---