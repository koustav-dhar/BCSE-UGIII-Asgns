#!/bin/sh
# Shell Script for Assignment 1 - Problem 4
cnt=0
for file in `find .`	# recursively surf all directories
do
  if [ -f "$file" ]	# check if it's a file or not
  then
    echo "$file"
    cnt=`expr $cnt + 1`	# increment files counter
  fi
done
echo "File Count: $cnt"
