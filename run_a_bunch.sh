#!/bin/bash

counter=1
lim=3 # default
# Launch a bunch of bash scripts
if [ "$#" -eq 1 ]; then
	lim=$1
fi

while [ $counter -le $lim ]; do
	xboard -cp -fcp "python3 xboard.py" -scp "python3 xboard.py" &
	((counter++))
done
