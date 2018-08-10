#!/bin/sh

THIS_DIR=`pwd`

## Benchmark instances from: https://www.sintef.no/projectweb/top/vrptw

proj_url=https://www.sintef.no/projectweb/top/vrptw
store_url=https://www.sintef.no/globalassets/project/top/vrptw/
solomon_url=http://web.cba.neu.edu/~msolomon

mkdir -p VRPTW
cd VRPTW

if true; then

mkdir -p homberger homberger-solutions

for n in 200 400 600 800 1000 ; do
	wget -c -O homberger_${n}.zip $store_url/homberger/${n}/homberger_${n}_customer_instances.zip
	unzip -d homberger -o homberger_${n}.zip
	# solutions
	wget -O homberger_${n}-solutions.html $proj_url/homberger-benchmark/${n}-customers/
	for s in `grep contentassets homberger_${n}-solutions.html | sed -e 's/^.*href=\"\/\(.*\)\.txt.*$/\1.txt/' ` ; do
		wget -c -O homberger-solutions/`basename $s`.solution http://www.sintef.no/$s
	done
done

for f in `ls homberger/*.TXT` ; do
	mv $f `echo $f | tr [:upper:] [:lower:]`
done

fi  # true/false enabler

# Solomon first 25, 50, 100 for 3 different instance sets

if true ; then

wget -c $store_url/solomon/solomon-100.zip
unzip -o solomon-100.zip

mkdir -p solomon

in_files=`ls In/*.txt`
for f in $in_files ; do
	o=`echo $f | sed -e 's/^.*\/\([a-z0-9]\+\)\.txt$/\U\1/'`
	cp $f solomon/$o.txt
	cp $f solomon/$o.100.txt
	lines=`cat $f | wc -l`
	for n in 25 50; do
		head -n $(($lines - (100 - $n))) $f > solomon/$o.$n.txt
	done
done

rm -rf In

# Solomon's solutions
wget -c $solomon_url/r1r2solu.htm -O solomon_r1r2-solutions.html
wget -c $solomon_url/c1c2solu.htm -O solomon_c1c2-solutions.html
wget -c $solomon_url/rc12solu.htm -O solomon_rc12-solutions.html
wget -c $solomon_url/heuristi.htm -O solomon_heuristi-solutions.html

fi  # true/false enabler

cd $THIS_DIR

##  TSPTW instances from: http://homepages.dcc.ufmg.br/~rfsilva/tsptw

if true ; then

proj_url=http://homepages.dcc.ufmg.br/~rfsilva/tsptw
mkdir -p TSPTW
cd TSPTW

# get instances
mkdir -p ins
for f in DaSilvaUrrutia DumasEtAl GendreauEtAl OhlmannThomas ; do
	wget -c $proj_url/$f.tar.gz
	tar xzf $f.tar.gz -C ins
done

# get fixed and missed instances
rm ins/n100w20.001.txt
wget -P ins $proj_url/ins/n100w20.001.txt

for n in 20 40 60 80 ; do
	for s in 001 002 003 004 005 ; do
		urls="$urls ${proj_url}/ins/n${n}w100.${s}.txt"
	done
done
wget -c -P ins $urls

# get solutions
wget -c http://homepages.dcc.ufmg.br/~rfsilva/tsptw -O tsptw-solutions.html
wget -np -nd -r -P solution -R index.html'*' $proj_url/solution/

cd $THIS_DIR

fi  # false/true enabler

## Instances from: http://myweb.uiowa.edu/bthoa/TSPTWBenchmarkDataSets.htm

# Dumas DumasExtend(Gendreau) and OhlmannThomas sets are identical to
# TSPTW's ones from above.
# SolomonTSPTW and Langevin sets (1) use different format, (2) don't have
# published solution.
# Based on above disable it for now

if false ; then

proj_url=http://myweb.uiowa.edu/bthoa/DownloadItems

mkdir -p UIOWA
cd UIOWA

for f in SolomonTSPTW Langevin ; do
	wget -c $proj_url/$f.zip
	unzip -o $f.zip
done

rm -rf __MACOSX

cd $THIS_DIR

fi  # false/true enabler
