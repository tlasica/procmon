__author__ = 'tomek'

import subprocess

def start_sar_command(cmd_str, interval_sec, out_dir, out_filename):
    out_path = '/'.join([out_dir, out_filename])
    cmd = cmd_str.split(' ')
    cmd += [str(interval_sec)]
    with open(out_path, 'w') as f_out:
        return subprocess.Popen(cmd, stdout=f_out, stderr=f_out)

#TODO: make subdirectories for os and pids
def start_os_monitoring(out_dir, interval_sec):
    spawns = []
    spawns.append( start_sar_command('sar -u ALL', interval_sec, out_dir, "os_cpu.log") )
    spawns.append( start_sar_command('sar -r', interval_sec, out_dir, "os_mem.log"))
    spawns.append( start_sar_command( 'sar -b', interval_sec, out_dir, "os_io.log"))
    spawns.append( start_sar_command('sar -S', interval_sec, out_dir, "os_swap.log"))
    spawns.append( start_sar_command( 'sar -w', interval_sec, out_dir, "os_processes.log"))
    spawns.append( start_sar_command('sar -n DEV', interval_sec, out_dir, "os_devices.log"))
    spawns.append( start_sar_command('sar -n SOCK', interval_sec, out_dir, "os_sockets.log"))
    spawns.append( start_sar_command('vmstat -n -S M', interval_sec, out_dir, "os_vmstat.log")) 
    return spawns

def pid_log_filename(pid, name):
    return "%d_%s.log" % (pid, name)


def start_sar_pid_command(cmd_str, pid, interval_sec, out_dir, out_filename):
    pid_cmd_str = cmd_str + " -p %d" %(pid)
    return start_sar_command(pid_cmd_str, interval_sec, out_dir, out_filename )

def start_pid_monitoring(out_dir, interval_sec, pid):
    popens = []
    popens.append( start_sar_pid_command('pidstat -u', pid, interval_sec, out_dir, pid_log_filename(pid, "cpu")) )
    popens.append( start_sar_pid_command('pidstat -r', pid, interval_sec, out_dir, pid_log_filename(pid, "mem")) )
    popens.append( start_sar_pid_command('pidstat -d', pid, interval_sec, out_dir, pid_log_filename(pid, "io")) )
    popens.append( start_sar_pid_command('pidstat -w', pid, interval_sec, out_dir, pid_log_filename(pid, "ctxs")) )
    return popens
