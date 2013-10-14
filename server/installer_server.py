#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import json
from profile_manager import Profile, ProfileManager
from repo_manager import RepoManager


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

    def ensure_mysql_connection(self):
        if self.mysql_conn == None:
            conn = self.mysql_connect()
            if conn == None:
                raise Exception("Cannot connect to mysql server")
            self.mysql_conn = conn
        else:
            self.mysql_conn.ping()

    def get_profiles_list(self):
        prof = ProfileManager()
        self.ensure_mysql_connection()
        return prof.get_profiles_list(self.mysql_conn)

    def get_repo_list(self):
        r = RepoManager()
        self.ensure_mysql_connection()
        return r.get_repo_list(self.mysql_conn)

    def add_repo(self, name, url):
        r = RepoManager()
        self.ensure_mysql_connection()
        r.add_repo(name, url, self.mysql_conn)

    def get_repo_by_id(self,id):
        r = RepoManager()
        self.ensure_mysql_connection()
        return r.get_repo_by_id(id, self.mysql_conn)

    def accept_server_info(self, info):
        raise NotImplementedError("Not implemented yet")

    def update_repo(self, id, name, url):
        r = RepoManager()
        self.ensure_mysql_connection()
        return r.edit_repo(id, name, url, self.mysql_conn)

    def delete_repo(self, id):
        r = RepoManager()
        self.ensure_mysql_connection()
        return r.delete_repo_by_id(id, self.mysql_conn)

    def get_profile_by_name(self, name):
        prof = ProfileManager()
        self.ensure_mysql_connection()
        p = prof.get_profile_by_name(name, self.mysql_conn)
        assert isinstance(p, Profile)
        return p.to_dict()

