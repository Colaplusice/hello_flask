#!/usr/bin/env bash

if [ "$(uname)"=="Darwin" ];
then
    echo "tis is mac"
 # Mac OS X 操作系统

elif [ "$(expr substr $(uname -s) 1 5)"=="Linux" ];
then
    echo"this is lunx"
# GNU/Linux操作系统

elif [ "$(expr substr $(uname -s) 1 10)"=="MINGW32_NT" ];
    then
 # Windows NT操作系统
 echo "this is windows"

fi
