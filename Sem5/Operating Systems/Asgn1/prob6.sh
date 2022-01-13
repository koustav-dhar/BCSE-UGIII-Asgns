#!/bin/bash
# Shell Script for Assignment 1 - Problem 6
get_day()
{
  t=( 0 3 2 5 0 3 5 1 4 6 2 4 )
  d=$1
  m=$2
  y=$3
  if [ "$m" \< "3" ]; then
    y=`expr $y - 1`
    #y=$(echo "$y - 1" | bc)
  fi
  index=`expr $m - 1`
  #index=$(echo "$m - 1" | bc)
  v=${t[index]}
  val=`expr $y + $y / 4 - $y / 100 + $y / 400 + $v + $d`
  #val=$(echo "$y + $y / 4 - $y / 100 + $y / 400 + $v + $d" | bc)
  val=`expr $val % 7`
  #val=$(echo "$val % 7" | bc)
  return $val
}

echo "Enter dates in format DD/MM/YYYY"
echo "Enter first birthday:"
read bday1
echo "Enter second birthday:"
read bday2
d1=$(echo "${bday1:0:2}")
d2=$(echo "${bday2:0:2}")
m1=$(echo "${bday1:3:2}")
m2=$(echo "${bday2:3:2}")
y1=$(echo "${bday1:6:4}")
y2=$(echo "${bday2:6:4}")
#echo "$d1 $m1 $y1    $d2 $m2 $y2"
get_day $d1 $m1 $y1
day1=$?
echo $day1
get_day $d2 $m2 $y2
day2=$?
echo $day2
if [ $day1 -eq $day2 ]; then
  echo "Both birthdays share same weekday!"
else
  echo "The birthdays occur on different weekdays."
fi
