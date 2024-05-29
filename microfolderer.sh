#!/bin/bash
punct (){
	echo "#############################################################################"
	echo "$1 complete"
	echo "#############################################################################"
}


for FILE in *.*
do
	TRUNK="${FILE%_*}"
	mkdir ur_cu_$TRUNK
	mv -i $FILE ur_cu_$TRUNK
done
punct "monroe"
