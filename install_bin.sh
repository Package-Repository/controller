#!/bin/bash

mkdir -p $HOME/ROBOT_LIB
destination_dir="$HOME/ROBOT_LIB"

cp can_driver "$destination_dir"
cp joy "$destination_dir"

echo "Copied binary files to $destination_dir"
