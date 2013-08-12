#!/usr/bin/python

import re

def isParam(line):
    if re.findall("^\s*[a-zA-Z0-9_\-]+\s*=\s*?",line):
	return 1;
    else:
	return 0;

def isGroup(line):
    if re.findall("^\s*\[\s*?(.*?)\s*?\]",line):
	return 1;
    return 0;

def getParam(line):
    return re.findall("^\s*([a-zA-Z0-9_\-]+)\s*=\s*?",line)[0];

def getGroupName(line):
    return re.findall("\[\s*(.*?)\s*\]",line)[0];

def stripComments(line):
    return re.sub(r'\s*?#.*?$','',line);

def getTokens(line):
    part = re.sub(".*?=","",line);
    result = [];
    flag = 1;
    raw = re.findall("((^|\s)\s*([\w/\-_\.#]+|\"([^\"]+)\"))",part);
    for i in raw:
	if flag != 0:
	    if i[len(i) - 1]:
		result += [i[len(i) - 1]];
	    else:
		rr = re.findall("[#]+",i[len(i) - 2]);
		if rr:
		    res = re.findall("(.*?)#",i[len(i) - 2]);
		    if res[0]:
			result += [res[0]];
		    flag = 0;
		else:
		    result += [i[len(i) - 2]];
    return result;

def parse(path):
    file = open(path,"r");
    result = {};
    sub = "";
    for line in file:
	if isGroup(line):
	    sub = getGroupName(line);
	    result[sub] = {};
	if isParam(line):
	    if sub:
		result[sub][getParam(line)] = getTokens(line);
	    else:
		result[getParam(line)] = getTokens(line);
    file.close();
    return result;

