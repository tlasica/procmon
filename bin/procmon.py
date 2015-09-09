import os
import threading

import subprocess

from datetime import datetime
import time

import logging
from logging import error, info, debug, exception, warning


def check_command_execution(cmd_and_params):
    try:
        with open(os.devnull, 'w') as devnull:
            subprocess.call(cmd_and_params, stdout=devnull, stderr=devnull)
        return True
    except OSError as exc:
        info("OSError when executing %s", str(cmd_and_params))
        return False
    except Exception as exc:
        error("Unexpected exception when executing: %s", str(cmd_and_params))
        error("Exception: %s" + str(exc))
        return False


def create_out_dir():
    now_str = datetime.now().isoformat().split('.')[0].replace("-","").replace(":","").replace("T","_")
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



def main(interval_sec):

    print "Checking if sysstat is installed and in path..."
    sysstat_ok = check_command_execution(['ssar', '-V'])
    if not sysstat_ok:
        return stop_execution(1, "Sysstat not installed or sar not in path or permission problem.")

    print "Finished"
    return 0

import sys, argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='interval', default="1", help = "monitoring interval in sec.")
    args = parser.parse_args()

    interval_sec = integer(args.interval)
    sys.exit(main(interval_sec))
