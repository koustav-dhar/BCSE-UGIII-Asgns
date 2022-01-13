#!/bin/sh
# Shell Script for Assignment 1 - Problem 8
echo "Enter file name to be read: "
read filename
echo "Enter word to be searched: "
read word
echo "Enter word which will replace the searched word: "
read replace
cnt=0
lno=1
while read fline
do
  lcnt=0
  for fword in $fline
  do
    if [ "$fword" = "$word" ]
    then
        lcnt=`expr $lcnt + 1`
    fi
  done
  if [ "$lcnt" -gt "0" ]
  then
      echo "Occurences in Line $lno: $lcnt"
      cnt=`expr $cnt + $lcnt`
  fi
  lno=`expr $lno + 1`
done < $filename
if [ "$cnt" -gt "0" ]
then
    echo "Total Occurences: $cnt"
    sed -i "s/$word/$replace/g" $filename
    echo "All occurences replaced successfully"
fi
if [ "$cnt" = "0" ]
then
    echo "No occurence found"
fi
