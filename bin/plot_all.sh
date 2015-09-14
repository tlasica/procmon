# Plot CPU for each process
for f in $(ls -1 [0-9]*cpu.*.log)
do 
  $(dirname $0)/plot_pid_cpu.sh $f
done

# Plot RAM for each process
for f in $(ls -1 [0-9]*mem.*.log)
do 
  $(dirname $0)/plot_pid_mem.sh $f
done

# Plot OS CPU
DATA_FILE=os_cpu.log
TMP_FILE=$DATA_FILE.tmp
$(dirname $0)/prepare_file.sh $DATA_FILE > $TMP_FILE
octave -f $(dirname $0)/plot_os_cpu.m $TMP_FILE $DATA_FILE.png
rm $TMP_FILE
