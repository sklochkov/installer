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
			c.close()
		except Exception, ex:
			c.close()
			raise DatabaseException("Failed to retrieve repo list: %s" % ex)
		for repo in repos:
			result.append({
				"id": repo[0],
				"name": repo[1],
				"value": repo[2]
			})
		return result	

	def repo_exists(self, conn, name=None, id=None):
		c = conn.cursor()
		if id != None:
			res = c.execute(REPO_GET_BY_ID_QUERY, (id,))
			if res.fetchone() == None:
				c.close()
				return False
			c.close()
			return True
		elif name != None:
			res = c.execute(REPO_GET_BY_NAME_QUERY, (name,))
                        if res.fetchone() == None:
                                return False
                        return True
		else:
			raise DataException("Neither id nor name of repository provided")

	def add_repo(self, name, url, conn):
		if self.repo_exists(conn, name=name):
			raise DataException("Repository %s already exists" % name)
		try:
			c = conn.cursor()
			c.execute(REPO_ADD_QUERY, (name, url))
			conn.commit()
			c.close()
			return conn.insert_id()
		except Exception, ex:
			conn.rollback()
                        c.close()
                        raise DatabaseException("Failed to add repo name=%s: %s" % (name, ex))
		
	def edit_repo(self, id, name, url, conn):
		try:
			c = conn.cursor()
			c.execute(REPO_UPDATE_QUERY, (name, url, id))
			conn.commit()
		except Exception, ex:
			conn.rollback()
                        c.close()
                        raise DatabaseException("Failed to update repo name=%s: %s" % (name, ex))
		return True

	def delete_repo(self, conn, id=None, name=None):
		if id != None:
			return self.delete_repo_by_id(id, conn)
		elif name != None:
			return self.delete_repo_by_name(name, conn)
		else:
			raise DataException("Neither id nor name of condemned repository provided")

	def delete_repo_by_id(self, id, conn):
		try:
			c = conn.cursor()
			c.execute(REPO_DROP_BY_ID_QUERY, (id,))
		except Exception, ex:
                        conn.rollback()
                        c.close()
                        raise DatabaseException("Failed to delete repo id=%s: %s" % (id, ex))
		try:
			c.execute(REPO_DROP_DEPS_BY_ID, (id,))
		except Exception, ex:
                        conn.rollback()
                        c.close()
                        raise DatabaseException("Failed to delete repo id=%s dependencies: %s" % (id, ex))
		try:
			conn.commit()
		except Exception, ex:
			conn.rollback()
			c.close()
			raise DatabaseException("Failed to commit deletion of repo id=%s dependencies: %s" % (id, ex))
		c.close()
		return True
		

	def delete_repo_by_name(self, name, conn):
                repo = self.get_repo_by_name(name, conn)
		return self.delete_repo_by_id(repo['id'], conn)

	def get_repo_by_id(self, id, conn):
		try:
			c = conn.cursor()
			res = c.execute(REPO_GET_BY_ID_QUERY, (id,))
			repo = res.fetchone()
		except Exception, ex:
			c.close()
                        raise DatabaseException("Failed to get repo by id=%s: %s" % (id, ex))
		return {
			'id': repo[0],
			'name': repo[1],
			'url': repo[2]
		}

	def get_repo_by_name(self, name, conn):
                try:
                        c = conn.cursor()
                        res = c.execute(REPO_GET_BY_NAME_QUERY, (name,))
                        repo = res.fetchone()
                except Exception, ex:
                        c.close()
                        raise DatabaseException("Failed to get repo by name=%s: %s" % (name, ex))
                return {
                        'id': repo[0],
                        'name': repo[1],
                        'url': repo[2]
			}
	
		

