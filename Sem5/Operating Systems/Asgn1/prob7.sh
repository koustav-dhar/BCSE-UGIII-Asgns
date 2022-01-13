#!/bin/sh
# Shell Script of Assignment 1 - Problem 7
echo "Enter a number to get it's multiplication table:"
read num
echo "Enter limit of multiplication table (enter a positive integer):"
read lim
i=0
while [ "$i" -lt "$lim" ]
do
  i=`expr $i + 1`
  echo "$num x $i = `expr $num \* $i`"
done
