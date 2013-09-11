#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import json


class InstallerServer:
	def __init__(self, mysql_host, mysql_user, mysql_pass, mysql_db):
		self.mysql_host = mysql_host
		self.mysql_user = mysql_user
		self.mysql_pass = mysql_pass
		self.mysql_db = mysql_db
		self.mysql_conn = None
		try:
			self.ensure_mysql_connection()
		except:
			# TODO: logging
			pass

	def mysql_connect(self):
		try:
			return MySQLdb.connect(host=self.mysql_host, user=self.mysql_user, passwd=self.mysql_pass, db=self.mysql_db)
		except:
			# TODO: logging
			return None

	def ensure_mysql_connection():
		if self.mysql_conn == None:
			conn = self.mysql_connect()
			if conn == None:
				raise Exception("Cannot connect to mysql server")
			self.mysql_conn = conn
		else:
			self.mysql_conn.ping()

	


