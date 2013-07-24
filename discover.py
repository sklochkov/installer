#!/usr/bin/python

import urllib2
import urllib
import sys
import os
import subprocess
import json
import datetime
import time

CONFIG = "/etc/discover.conf"
DEFAULT_BASE = "http://192.168.10.169"

INFO_URI = "/discover/api/info"
CHECK_URI = "/discover/api/check"

LOG = '/var/log/discover.log'

# STUB
def get_my_mac():
	return "foo"

# STUB
def get_config()
	return {
		'base': DEFAULT_BASE
	}

def log(text):
	f = open(LOG, 'w')
	now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	f.write("%s %s " % (now, text))
	f.close()

# STUB
def reboot_me():
	pass 

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
		res = urllib2.urlopen(url,timeout=5)
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

# STUB
def get_ifaces_info():
	return {}

# STUB
def get_cpu_info():
	return {}

# STUB
def get_mem_info():
	return {}

# STUB
def get_disks_info():
	return {}

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
	if len(sys.argv < 2):
		usage()
		sys.exit(1)
	if sys.argv[1] == "check":
		check_reboot_flag()
	elif sys.argv[1] == "discover":
		while send_info() == False:
			time.sleep(10)
	else:
		usage()
                sys.exit(1)		


