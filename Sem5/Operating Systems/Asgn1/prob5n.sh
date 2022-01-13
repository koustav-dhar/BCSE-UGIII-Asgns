#!/bin/bash
# Shell Script for Assigment 1 - Problem 5

dir=my-deleted-files
dfile=$1
if [ -f $dfile ]; then
  echo "Deleting..."
elif [ "$dfile" = "-c" ]; then
  cd $dir
  rm *
  cd ..
  echo "Successfully cleared trash."
  exit
else
  echo "File $dfile does not exist. Aborting..."
  exit
fi
dfilename="${dfile%.*}"
dfileextn="${dfile##*.}"
ver=0

cd $dir
checkfile="${dfilename}_0.${dfileextn}"
if [ -f $dfile ]; then
  firstfile="${dfilename}_0.${dfileextn}"
  mv $dfile $firstfile
elif [ -f $checkfile ]; then
  :
else
  cd ..
  mv $dfile $dir
  echo "Successfully deleted."
  exit
fi

find ${dfilename}*.${dfileextn} | ( while read file
do
  filename="${file%.*}"
  filecomp="${filename%_*}"
  if [ $dfilename != $filecomp ]; then
    continue
  fi
  curver=${filename#*_}
  if [ $curver -gt $ver ]; then
    ver=$curver
  fi
done
cd ..
ver=`expr $ver + 1`
nfile="${dfilename}_${ver}.${dfileextn}"
mv $dfile $nfile
mv $nfile $dir )
echo "Successfully deleted."
