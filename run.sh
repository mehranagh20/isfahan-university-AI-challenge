#!/bin/bash

loc=$(pwd)

cd $loc/server/src
python3 -u $loc/server/src/Main.py > $loc/log/server-log 2> $loc/log/server-errors &
echo $! >> $loc/pids
echo "server started"
cd $loc

sleep 1

python3 -u $loc/alirez/no-one/Main.py > $loc/log/enemy-log 2> $loc/log/enemy-errors &
echo $! >> $loc/pids
echo "enemy joined"

python3 -u $loc/me/no-name/Main.py > $loc/log/me-log 2> $loc/log/me-errors &
echo $i >> $loc/pids
echo "you joined"

sleep 2

if [[ "$1" == "g" ]]; then
    java -jar $loc/gui/gui.jar $loc/server/src/log
fi

for i in $(cat pids); do
    kill $i 2> /dev/null
done

echo "" > pids

gedit $loc/log/me-errors &
gedit $loc/log/me-log &

pkill python3
