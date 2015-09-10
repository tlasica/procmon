# Genymotion Process Monitor

The tool uses sysstat tools sar and pidstat to:

1. log system metrics (cpu, mem, io, net, ctxswitch etc.)
2. log cpu/mem/io metrics for specified processes (pids)
3. automatically start tracking processes of given naming patterns like 'player' or 'VBox'
4. plot all charts for logged data with one command

# Installation

Sysstat has to be installed and running:

    sudo apt-get install sysstat

Now running

    sar -u 1 3

Should show some cpu statistics to verify systtat works correctly.

# Usage

Basic usage pattern is to start the tool before benchmark or test is started
and ask for auto monitoring of interesting genymotion processes:

    python bin/procMon.py --auto -i 5 --r 120

Will run the tool with 5s interval for 120 rounds, which is 10 minutes.
After this time script will stop.

During the execution script will test for new player or vbox processes
and once detected will start logging their cpu/mem/io metrics.


# Output

Output is generated in a separate directory for each run of the script.
Directory is created in a *out* subfolder and named with the timestamp of starting the script.

Output directory will include:

* *os_xxx.log* files for general system metrics
* *{PID}_xxx.log* files for genymotion procesesses

# Plots

Plots (not implemented yet) can be generated offline.

ProcMon uses *octave* to plot charts from the logged sar/pidstat outputs:

    sudo apt-get install octave
