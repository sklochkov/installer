#!/usr/bin/python

import urllib2
import urllib
import sys
import subprocess
import json
import datetime
import time
import re

CONFIG = "/etc/discover.conf"
DEFAULT_BASE = "http://192.168.10.169"

INFO_URI = "/discover/api/info"
CHECK_URI = "/discover/api/check"

LOG = '/var/log/discover.log'

# STUB

"""
[root@foo~]# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 16436 qdisc noqueue state UNKNOWN
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP qlen 1000
    link/ether 00:25:90:85:6c:98 brd ff:ff:ff:ff:ff:ff
    inet 10.72.0.9/16 brd 10.72.255.255 scope global eth0
    inet6 fe80::225:90ff:fe85:6c98/64 scope link
       valid_lft forever preferred_lft forever
3: eth1: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN qlen 1000
    link/ether 00:25:90:85:6c:99 brd ff:ff:ff:ff:ff:ff
"""

ETH_RE = re.compile("""^\d+:\s+(eth\d+):.*?state\s+(.*?)\s+qlen.*?$""")
MAC_RE = re.compile("""^\s+link/ether\s+(.*?)\s+brd.*?$""")

"""
model name      : Intel(R) Xeon(R) CPU E3-1270 V2 @ 3.50GHz
"""

CPU_RE = re.compile("""^model name\s+:\s+(.*?)$""")

"""
[root@foo~]# cat /proc/partitions
   8        0  976762584 sda
   8        1   61440000 sda1
   8        2  915320832 sda2
   8       16  976762584 sdb
   8       17   61440000 sdb1
   8       18  915320832 sdb2
   8       32  976762584 sdc
   8       33   61440000 sdc1
   8       34  915320832 sdc2
   8       48  976762584 sdd
   8       49   61440000 sdd1
   8       50  915320832 sdd2
   9        0   61439928 md0
   9        1   61438908 md1
   9        2 1830638592 md2
"""

PART_RE = re.compile("""^\s+\d+\s+\d+\s+(\d+)\s+(.*?)$""")

def get_my_mac():
    """
    @rtype : unicode
    """
    p = subprocess.Popen(args="/sbin/ip addr", shell=True, stdout=subprocess.PIPE)
    flg = 0
    for line in p.stdout:
        res = ETH_RE.match(line)
        if res and res.group(2) == 'UP':
            flg = 1
        elif flg == 1:
            res2 = MAC_RE.match(line)
            if res2 and res2.group(1):
                return res2.group(1)
    return None

def get_config():
    return {
        'base': DEFAULT_BASE,
        'info_uri': INFO_URI,
        'check_uri': CHECK_URI
    }

def log(text):
    f = open(LOG, 'w')
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    f.write("%s %s " % (now, text))
    f.close()

def reboot_me():
    f = open('/proc/sysrq-trigger', 'w')
    f.write('b\n')
    # We are not supposed to get here, but...
    raise Exception("Failed to initiate reboot")

def check_reboot_flag():
    try:
        cfg = get_config()
    except Exception, ex:
        log("[check] Exception while reading config: %s" % str(ex))
        return False
    try:
        mac = get_my_mac()
    except Exception, ex:
        log("[check] Exception while getting mac address: %s" % str(ex))
        return False
    params = urllib.urlencode({'mac': mac})
    url = "%s%s?%s" % (cfg['base'], CHECK_URI, params)
    try:
        res = urllib2.urlopen(url, timeout=5)
        reply = res.read()
        res.close()
    except Exception, ex:
        log("[check] Exception while getting commands: %s" % str(ex))
        return False
    try:
        if reply.strip() == 'reboot':
            reboot_me()
            return True # LOL
    except Exception, ex:
        log("[check] Exception while rebooting: %s" % str(ex))
    return False

def collect_info():
    mac = get_my_mac()
    ifaces = get_ifaces_info()
    cpu = get_cpu_info()
    mem = get_mem_info()
    disks = get_disks_info()
    return {
        'mac': mac,
        'ifaces': ifaces,
        'cpu': cpu,
        'mem': mem,
        'disks': disks
    }

def get_ifaces_info():
    p = subprocess.Popen(args="/sbin/ip addr", shell=True, stdout=subprocess.PIPE)
    flg = 0
    result = ""
    i = 0
    for line in p.stdout:
        #print line
        if flg == 0:
            res = ETH_RE.match(line)
            if res:
                #print "1 ", res.group(1), res.group(2)
                #result.append({
                #    'name': res.group(1),
                #    'status': res.group(2)
                #})
                result += "%s: %s" % (res.group(1), res.group(2))
                flg = 1
        elif flg == 1:
            res2 = MAC_RE.match(line)
            if res2 and res2.group(1):
                #print "2 ", res2.group(1)
                #result[i]['mac'] = res2.group(1)
                result += " (%s)\n" % res2.group(1)
            flg = 0
            i += 1
    return result

def get_cpu_info():
    result = ""
    f = open('/proc/cpuinfo', 'r')
    for line in f:
        res = CPU_RE.match(line)
        if res:
            result += "%s\n" % res.group(1)
    f.close()
    return result

def get_mem_info():
    result = "0"
    f = open('/proc/meminfo', 'r')
    res = f.readline()
    result = res.split('    ')[-1].split(' ')[0]
    f.close()
    return result

def get_disks_info():
    result = ""
    f = open('/proc/partitions','r')
    for line in f:
        res = PART_RE.match(line)
        if res:
            result += "%s %s\n" % (res.group(2), res.group(1))
    f.close()
    return result

def send_info():
    try:
        cfg = get_config()
    except Exception, ex:
        log("[discover] Exception while reading configuration: %s" % str(ex))
        return False
    try:
        info = collect_info()
    except Exception, ex:
        log("[discover] Exception while reading server info: %s" % str(ex))
        return False
    data = urllib.urlencode({'info': json.dumps(info)})
    url = "%s%s" % (cfg['base'], INFO_URI)
    try:
        res = urllib2.urlopen(url, data=data, timeout=10)
        reply = res.read()
        res.close()
        if reply.strip() == "ok":
            return True
        else:
            log("[discover]: incorrect reply from server %s: %s" % (url, reply.strip()))
            return False
    except Exception, ex:
        log("[discover] Exception while reading server info: %s" % str(ex))
        return False

def usage():
	print "discover.py <check|discover>"
	
if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)
    elif sys.argv[1] == "check":
        check_reboot_flag()
    elif sys.argv[1] == "discover":
        while send_info() == False:
            time.sleep(10)
    elif sys.argv[1] == "test":
        print "MAC address:\n", get_my_mac()
        print "\n\nInterfaces\n", get_ifaces_info()
        print "\n\nCPU\n", get_cpu_info()
        print "\n\nMemory\n", get_mem_info()
        print "\n\nDisks\n", get_disks_info()
    else:
        usage()
        sys.exit(1)


