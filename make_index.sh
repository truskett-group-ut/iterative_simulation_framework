#!/bin/bash

rm indexmaker.txt
touch indexmaker.txt
echo "keep 0" >> indexmaker.txt
icount=1
for i in A B C D E F G H I J K L M N O P Q R S T U V W X Y Z; do 
    echo "a" $i >> indexmaker.txt
    let icount+=1
    if [ $icount -gt $1 ]; then
       break
    fi
done
echo "q" >> indexmaker.txt
gmx make_ndx -f conf.gro < indexmaker.txt
rm indexmaker.txt
