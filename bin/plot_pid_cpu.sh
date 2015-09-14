DATA_FILE=$1
TMP_FILE=$DATA_FILE.tmp
$(dirname $0)/prepare_file.sh $DATA_FILE > $TMP_FILE
octave -f $(dirname $0)/plot_pid_cpu.m $TMP_FILE $DATA_FILE.png
rm $TMP_FILE


