#!/bin/bash
# Shell Script for Assigment 1 - Problem 5

dir=my-deleted-files
dfile=$1    # extracting the first command line argument
if [ -f $dfile ]; then  # if it's a file name
  echo "Deleting..."
elif [ "$dfile" = "-c" ]; then  # clear trash if -c flag
  cd $dir
  rm *
  cd ..
  echo "Successfully cleared trash."
  exit
else
  echo "File $dfile does not exist. Aborting..."  # if file doesn't exist
  exit
fi
dfilename="${dfile%.*}"   # extracting only filename part
dfileextn="${dfile##*.}"  # extracting only file extension
ver=0

cd $dir
checkfile="${dfilename}_0.${dfileextn}"
if [ -f $dfile ]; then    # check if only occurence exists
  firstfile="${dfilename}_0.${dfileextn}"   # rename the first occurence with _0
  mv $dfile $firstfile
elif [ -f $checkfile ]; then
  :
else                      # else if this is the first occurence
  cd .. 
  mv $dfile $dir
  echo "Successfully deleted."
  exit
fi

find ${dfilename}*.${dfileextn} | ( while read file   # traverse through all deleted files with similar name
do
  filename="${file%.*}"   # extract only file name part
  filecomp="${filename%_*}"
  if [ $dfilename != $filecomp ]; then  # check if filename same or not
    continue
  fi
  curver=${filename#*_}   # extract the version number
  if [ $curver -gt $ver ]; then   # get the latest version
    ver=$curver
  fi
done
cd ..
ver=`expr $ver + 1`       # update the new version
nfile="${dfilename}_${ver}.${dfileextn}"  # construct new filename
mv $dfile $nfile          
mv $nfile $dir )          
echo "Successfully deleted."
