#!/bin/bash

TEST_SPECINT=yes
TEST_SPECFP=yes

#SPEC_DIR=speccpu2006
#cd $SPEC_DIR
cd ../

. ./shrc

if [ "$TEST_SPECINT" = "yes" ]; then
	./bin/runspec -c e5-2640v4.cfg int --rate 1 -n 1 --noreportable
	#./bin/runspec -c e5-2640v4.cfg int --rate 20 -n 1 --noreportable
	./bin/runspec -c e5-2640v4.cfg int --rate 40 -n 1 --noreportable
fi

if [ "$TEST_SPECFP" = "yes" ]; then
	./bin/runspec -c e5-2640v4.cfg fp --rate 1 -n 1 --noreportable
	#./bin/runspec -c e5-2640v4.cfg fp --rate 20 -n 1 --noreportable
	./bin/runspec -c e5-2640v4.cfg fp --rate 40 -n 1 --noreportable
fi
