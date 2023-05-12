#!/bin/bash

NTHREADS=12

for (( i=0; i<$NTHREADS; i++ ))
do
    gnome-terminal -- python stability.py --nthreads $NTHREADS --thread_id $i --stage preproc &
done
