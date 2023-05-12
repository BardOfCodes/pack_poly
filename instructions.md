# Instructions for running the code

## Installation

Please install the required pacakges with

```bash
X
# Add folder path to PYTHONPATH
export $FOLDERPATH=<your-folder-path>

export PYTHONPATH="$FOLDERPATH:$PYTHONPATH"
cd $FOLDERPATH
```

## 1. Testing Packing

You can run the packing tests with:

```bash
python scripts/test_cases.py
```

## 2 Packing for Logic

You can run the solver to create the "LOGIC" packing with:

```bash
source scripts/run_logic.sh
# Which runs python scripts/generate_logic.py in 5 threads

```

This will create 5 `.png` files in `outputs` corresponding to the 5 letters.

## 3 Stability

We compute our stability scores in two steps. First, given the board, we compute the solution for all possible valid polyomino combinations.

```bash
source scripts/run_stability.sh
# Which calls python scripts/stability.py --nthreads $NTHREADS --thread_id $i --stage preproc
```

Each thread saves the solutions for a partion of the polyomino combinations. Next, we use the saved solutions, to compute the stability measure for different amounts of perturbations by:

```bash
python scripts/stability.py
```

This script creates visualization of the top 3 highest stability configurations, and saved them in `./stability_out/`

Finally, we can render our final results as a gif with:

```bash
python scripts/visualize_stability.py

```

This will save a `.gif` visualizing the highest stability configuration, with textures at `outputs/gif_stability/`.
