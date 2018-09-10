#!/bin/bash

PID_FILE=$1
FILE_TO_SAVE=$2

if [ "$#" -eq 0 ] ; then
  echo "Illegal number of parameters"
  echo "missing (1) PID file like /tmp/file.pid"
  echo "missing (2) file to keep values collected like /home/$USER/cpu-memory.txt"
  exit 1
fi

# wait for the creation of PID file
while [ ! -f "$PID_FILE" ]
do
  sleep 1
done

# show PID
cat $PID_FILE

# get PID number
PID=$(cat "$PID_FILE")

# get CPU and memory consumption from ps, similar to command 'top'
VALUES=$(ps -p $PID -o %cpu,%mem | tail -n 1)

# write values to file
while [[ $VALUES != *"CPU"* ]]; do

  if [ -z $FILE_TO_SAVE ]; then
    echo "$VALUES"
  else
    echo "$VALUES" >> $FILE_TO_SAVE
  fi

  VALUES=$(ps -p $PID -o %cpu,%mem | tail -n 1)
  sleep 0
done
