#!/bin/bash

# A utility script to create blank inputs for a new AoC day.

# get arguments: -d (day number), -f (name for python file)
while getopts d:f: flag
do
    case "${flag}" in
        d) day_num=${OPTARG};;
        f) f_name=${OPTARG};;
    esac
done

# handle missing args case
if [ -z "$day_num" ] || [ -z "$f_name" ]; then
    echo 'Missing -d or -f' >&2
    exit 1
else
    # create data folder, text files, and empty python file for that day
    echo "Prepping for day number: $day_num"
    mkdir data/day_"$day_num"
    touch data/day_"$day_num"/input.txt
    touch data/day_"$day_num"/test_input.txt
    mkdir advent_of_code_2023/day_"$day_num"
    touch advent_of_code_2023/day_"$day_num"/"$f_name".py
fi
