#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
from my_exceptions import DatabaseException, DataException, InternalException
import json

REPO_GET_ALL_QUERY = """select `id`, `name`, `url` from `repositories`"""

REPO_GET_BY_ID_QUERY = """select `id`, `name`, `url` from `repositories` where `id` = %s"""

REPO_GET_BY_NAME_QUERY = """select `id`, `name`, `url` from `repositories` where `name` = %s"""

REPO_ADD_QUERY = """insert into `repositories` (`id`, `name`, `url`) values (NULL, %s, %s)"""

REPO_UPDATE_QUERY = """update `repositories` set `name` = %s, `url` = %s where `id` = %s"""

REPO_DROP_BY_ID_QUERY = """delete from `repositories` where `id` = %s"""

REPO_DROP_DEPS_BY_ID = """delete from `profiles_repositories` where `repo_id` = %s"""

class RepoManager:
	def __init__(self):
		pass

	def get_repo_list(self, conn):
		result = []
		try:
			c = conn.cursor()
			res = c.execute(REPO_GET_ALL_QUERY)
			repos = res.fetchall()
		except Exception, ex:
			c.close()
			raise DatabaseException("Failed to retrieve repo list: %s" % ex)
		for repo in repos:
			result.append({
				"id": repo[0],
				"name": repo[1],
				"value": repo[2]
			})
			

	def add_repo(self, name, url, conn):
		pass

	def edit_repo(self, id, name, url, conn):
		pass

	def delete_repo(self, conn, id=None, name=None):
		if id != None:
			return self.delete_repo_by_id(id, conn)
		elif name != None:
			return self.delete_repo_by_name(name, conn)
		else:
			raise DataException("Neither id nor name of condemned repository provided")

	def delete_repo_by_id(self, id, conn):
		pass

	def delete_repo_by_name(self, id, conn):
                pass

	def get_repo_by_id(self, id, conn):
		pass

	def get_repo_by_name(self, name, conn):
                pass

	
		

