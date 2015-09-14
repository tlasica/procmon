CMD=$1
ALIAS=$2
for FNAME in $(ls -1 [0-9]*.log | xargs grep -l $CMD)
do
  DSTNAME=`echo $FNAME|sed s/.log/.$ALIAS.log/`
  echo renaming $FNAME to $DSTNAME
  mv $FNAME $DSTNAME
done

