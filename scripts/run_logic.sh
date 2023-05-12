#!/bin/bash

NTHREADS=5

for (( i=0; i<$NTHREADS; i++ ))
do
    gnome-terminal -- python scripts/generate_logic.py --thread_id $i &
done
