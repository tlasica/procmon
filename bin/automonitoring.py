__author__ = 'tomek'

import threading, subprocess, time
from logging import debug

from sarhelper import start_pid_monitoring

def patterns():
    d = {}
    d['player'] = 'ps -C player -o pid='
    d['vbox'] = 'ps -C VBoxHeadless -o pid='
    return d

'''
Design decisions:
* keep map of monitored processes PID => {Popens}
*
'''
class MonitoringThread(threading.Thread):

    def __init__(self, out_dir, interval):
        self.out_dir = out_dir
        self.interval = interval
        self.stoprequest = threading.Event()
        self.monitored_pids = {}
        threading.Thread.__init__(self)

    def run(self):
        while not self.stoprequest.isSet():
            running_pids = self._find_running_pids(patterns())
            started_pids = self._start_pidstat_for_new_pids(running_pids)
            self.monitored_pids.update( started_pids )
            time.sleep(self.interval)

    def _find_running_pids(self, patterns):
        ret = []
        for (alias, cmd) in patterns.items():
            running = self._find_running_pids_with_command(cmd)
            debug("pids for %s: %s", alias, str(running))
            ret += running
        return ret

    def _find_running_pids_with_command(self, cmd):
        cmd_args = cmd.split(' ')
        out = subprocess.check_output(cmd_args)
        pids = out.split('\n')
        ret = []
        for s in pids:
            s_trim = s.replace(' ','')
            if s_trim and len(s_trim)>0:
                ret += [ int(s_trim) ]
        return ret

    def _start_pidstat_for_new_pids(self, pids):
        started = {}
        for pid in pids:
            if not self.monitored_pids.has_key(pid):
                print "Auto monitoring for pid %d started!" % (pid)
                started[pid] = start_pid_monitoring(self.out_dir, self.interval, pid)
        return started

    def _stopSarProcesses(self):
        for pids in self.monitored_pids.values():
            for pop in pids:
                pop.terminate()

    def join(self, timeout=None):
        self.stoprequest.set()
        self._stopSarProcesses()
        super(MonitoringThread, self).join(timeout)


