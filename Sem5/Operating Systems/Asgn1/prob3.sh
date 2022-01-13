#!/bin/sh
# Shell Script for Assignment 1 - Problem 3
lines=0
echo "Enter file name:"
read filename	# get the filename
while read input_text	# while loop to read the file line by line
do
  lines=`expr $lines + 1`	# increment counter
done < $filename
echo "No of lines in $filename: $lines"
