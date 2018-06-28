#!/bin/bash

TEST_SPECINT=yes
TEST_SPECFP=yes

#SPEC_DIR=speccpu2006
#cd $SPEC_DIR
cputype=`dmidecode -t processor | grep Version | awk -F ':' '{print $2}'`

cd ../

. ./shrc

if [ "$TEST_SPECINT" = "yes" ]; then
	#./bin/runspec -c hi1620.cfg int --speed -n 1 --noreportable
	#./bin/runspec -c 2650v4.cfg 471.omnetpp --rate 1 -n 1  --noreportable
	./bin/runspec -c hi1620.cfg int --rate 1 -n 1 --noreportable
	./bin/runspec -c hi1620.cfg int --rate 32 -n 1 --noreportable
	./bin/runspec -c hi1620.cfg int --rate 64 -n 1 --noreportable
fi

if [ "$TEST_SPECFP" = "yes" ]; then
	#./bin/runspec -c hi1620.cfg fp --speed -n 1 --noreportable
	./bin/runspec -c hi1620.cfg fp --rate 1 -n 1 --noreportable
	./bin/runspec -c hi1620.cfg fp --rate 32 -n 1 --noreportable
	./bin/runspec -c hi1620.cfg fp --rate 64 -n 1 --noreportable
fi
