#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
import config
import json
import installer_server
import logging

CONFIG = /etc/installer/installer.conf

class InstallerServerApp(flask.Flask):
        def __init__(self, *args, **kwargs):
                super(InstallerServerApp, self).__init__(*args, **kwargs)

app = InstallerServerApp(__name__)

@app.route('/discover/ping')
def ping():
	return "pong"

@app.route('/discover/api/info',methods=['POST'])
def accept_info():
	if 'info' not in flask.request.form:
		flask.abort(400)
	info_raw = flask.request.form['info']
	try:
		info = json.loads(flask.request.form['info'])
	except:
		flask.abort(400)
	try:
		installer_server.accept_info(info)
	except:
		flask.abort(500)
	return "Not implemented"

@app.route('/discover/profiles')
def profiles_list():
	return "Not implemented yet"


@app.route('/discover/profiles/add', methods=['POST'])
def add_profile():
	
