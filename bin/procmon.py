import os

import subprocess

from datetime import datetime
import time

from logging import error, info, debug, exception, warning


def check_command_execution(cmd_and_params):
    try:
        with open(os.devnull, 'w') as devnull:
            subprocess.call(cmd_and_params, stdout=devnull, stderr=devnull)
        return True
    except OSError as exc:
        error("OSError when executing %s", str(cmd_and_params))
        return False
    except Exception as exc:
        error("Unexpected exception when executing: %s", str(cmd_and_params))
        error("Exception: %s" + str(exc))
        return False


def create_out_dir():
    now_str = datetime.now().isoformat().split('.')[0].replace("-", "").replace(":", "").replace("T", "_")
    path = '/'.join(['out', now_str])
    try:
        os.makedirs(path)
        return (path, True)
    except OSError as exc:
        print exc
        return (path, False)


def metric_file_path_with_ext(out_dir, metric_alias, ext):
    fname = '.'.join([metric_alias, ext])
    return '/'.join([out_dir, fname])


#########################################################################################333
# MAIN
#########################################################################################333

def metrics_for_monitoring():
    metrics = []
    metrics.append(('clientRequest.Write.Latency.95Percentile',
                    'org.apache.cassandra.metrics:type=ClientRequest,scope=Write,name=Latency', '95thPercentile'))
    metrics.append(('keyspace1.standard1.AllMemtablesLiveDataSize',
                    'org.apache.cassandra.metrics:type=ColumnFamily,keyspace=keyspace1,scope=standard1,name=AllMemtablesLiveDataSize',
                    'Value'))
    metrics.append(('keyspace1.standard1.LiveSSTableCount',
                    'org.apache.cassandra.metrics:type=ColumnFamily,keyspace=keyspace1,scope=standard1,name=LiveSSTableCount',
                    'Value'))
    return metrics


def stop_execution(code, msg):
    print
    print msg
    print "Exit with " + str(code)
    return code

from automonitoring import MonitoringThread
from sarhelper import start_os_monitoring, start_pid_monitoring

def main(interval_sec, num_rounds, pids, automonitoring_on):

    print "Checking if sysstat is installed and in path..."
    sysstat_ok = check_command_execution(['sar', '-V'])
    if not sysstat_ok:
        return stop_execution(1, "Sysstat not installed or sar not in path or permission problem.")
    print "Checking if sysstat is installed and in path...OK"

    print "Creating output directory..."
    (out_dir, created) = create_out_dir()
    if created:
        print "..output directory: ", out_dir
    else:
        stop_execution(3, "Cannot create output directory.")
    print "Creating output directory...OK"

    print "Starting os level monitoring..."
    spawns = start_os_monitoring(out_dir, interval_sec)
    print "Starting os level monitoring...OK"

    if pids:
        for pid in pids.split(','):
            print "Starting monitoring for pid %s" % (pid)
            spawns += start_pid_monitoring(out_dir, interval_sec, int(pid))


    monitor = None
    if automonitoring_on:
        print "Automatic monitoring for interesting processes is ON"
        th = MonitoringThread(out_dir, interval_sec)
        th.setDaemon(True)
        th.start()
        monitor = th


    print "Sleeping for %s rounds of %s sec..." % (num_rounds, interval_sec)
    # no idea what to wait for, so let' sleep
    while num_rounds>0:
        time.sleep(interval_sec)
        num_rounds = num_rounds - 1

    # hmmm, should we not stop those?
    print "Stopping sar/pidstat processes..."
    for p in spawns:
        p.terminate()
    if monitor:
        monitor.join()
    print "Stopping sar/pidstat processes...OK"

    print "Finished"
    return 0

import sys, argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='interval', default="1", help="monitoring interval in sec (def 1).")
    parser.add_argument('-r', dest='rounds', default="1000", help="number of monitoring rounds (def 1000)")
    parser.add_argument('-p', dest='pids', default="", help="list of pids for monitoring")
    parser.add_argument('--auto', dest='automonitoring', action="store_true", help="auto monitoring of new processes")
    args = parser.parse_args()

    interval_sec = int(args.interval)
    num_rounds = int(args.rounds)
    sys.exit(main(interval_sec, num_rounds, args.pids, args.automonitoring))
