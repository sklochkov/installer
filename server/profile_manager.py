#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
from jinja2 import Template, Environment, PackageLoader
from my_exceptions import DatabaseException, DataException, InternalException
import json

PROFILE_ADD_QUERY = """insert into `profiles` (`id`, `name`, `status`) VALUES (NULL, %s, %s)"""
PROFILE_PARAMS_ADD_QUERY = """insert into `profile_parameters` (`id`, `profile_id`, `name`, `value`) VALUES (NULL, %s, %s, %s)"""

PROFILE_STATUS_UPDATE_QUERY = """update `profiles` set `status` = %s where `id` = %s"""
PROFILE_NAME_UPDATE_QUERY = """update `profiles` set `name` = %s where `id` = %s"""

PROFILE_PARAM_UPDATE_QUERY = """update `profile_parameters` set `value` = %s where `profile_id` = %s and `name` = %s"""

PROFILE_GET_QUERY = """select `profiles`.`id` as `prof_id`, `profiles`.`name` as `prof_name`, `profile_parameters`.`name` as `param.name`, `profile_parameters`.`value` as `param_value` from `profiles`, `profile_parameters` where `profiles`.`name` = %s and `profiles`.`id` = `profile_parameters`.`profile_id`"""
PROFILE_GET_REPOSITORIES_QUERY = """select `profiles`.`name` as `prof_name`, `repositories`.`name` as `repo_name`, `repositories`.`url` as `repo_url`, `repositories`.`id` as `repo_id` from `profiles`, `repositories`, `profiles_repositories` where `profiles`.`name` = %s and `profiles`.`id` = `profiles_repositories`.`profile_id` and `repositories`.`id` = `profiles_repositories`.`repo_id`"""

PROFILE_ID_BY_NAME_QUERY = """select `id` from `profiles` where `name` = %s"""

PROFILE_ADD_REPOSITORY_BINDINGS = """insert into `profiles_repositories` (`id`, `profile_id`, `repo_id`) values (NULL, %s, %s)"""

PROFILE_DROP_REPOSITORY_BINDINGS = """delete from `profiles_repositories` where `profile_id` = %s"""

PROFILE_LIST_QUERY = """select `name`, `status` from `profiles`"""


class Profile:
    def __init__(self, id=None, name="", installer_url="", network_settings="", disk_settings="", repos=[], packages="",
                 preinstall="", postinstall=""):
        self.id = id
        self.name = name
        self.installer_url = installer_url
        self.network_settings = network_settings
        self.disk_settings = disk_settings
        self.repos = repos
        self.packages = packages
        self.preinstall = preinstall
        self.postinstall = postinstall

    def to_kickstart(self):
        env = Environment(loader=PackageLoader('pattern', 'templates'))
        tmpl = env.get_template('kickstart.cfg')
        return tmpl.render(url=self.installer_url, network=self.network_settings, partitions=self.disk_settings,
                           repos=self.repos, packages=self.packages, preinstall=self.preinstall,
                           postinstall=self.postinstall)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'installer_url': self.installer_url,
            'network_settings': self.network_settings,
            'disk_settings': self.disk_settings,
            'repos': self.repos,
            'packages': self.packages,
            'preinstall': self.preinstall,
            'postinstall': self.postinstall
        }

    def to_json(self):
        return json.dumps(self.to_dict())


class ProfileManager:
    def __init__(self):
        pass

    def get_profile_by_name(self, name, conn):
        try:
            c = conn.cursor()
            c.execute(PROFILE_GET_QUERY, (name,))
            #res = c.fetchmany()
        except Exception, ex:
            c.close()
            raise DatabaseException("Error while trying to retrieve profile %s: %s" % (name, ex))
        try:
            params = {
                'installer_url': "",
                'network_settings': "",
                'disk_settings': "",
                'packages': "",
                'preinstall': "",
                'postinstall': "",
                'repos': [],
                'name': "",
                'id': None
            }
            for param in c:
                if param[2] in params:
                    params[param[2]] = param[3]
            params['name'] = param[1]
            params['id'] = param[0]
        except Exception, ex:
            c.close()
            raise InternalException("Error while processing profile parameters: %s" % str(ex))
        try:
            c.execute(PROFILE_GET_REPOSITORIES_QUERY, (name,))
            //res = c.fetchmany()
        except Exception, ex:
            #c.close()
            raise DatabaseException("Error while trying to retrieve profile %s: %s" % (name, ex))
        try:
            for repo in c:
                params['repos'].append({
                    'name': repo[1],
                    'url': repo[2],
                    'id': repo[3]
                })
            c.close()
        except Exception, ex:
            raise InternalException("Error while processing profile repository parameters: %s" % str(ex))
        try:
            profile = Profile(**params)
            return profile
        except Exception, ex:
            raise InternalException("Error while creating profile object: %s" % str(ex))

    def profile_exists(self, name, conn):
        try:
            c = conn.cursor()
            c.execute(PROFILE_ID_BY_NAME_QUERY, (name,))
            res = c.fetchone()
            c.close()
            if not res:
                return False
            return True
        except Exception, ex:
            raise DatabaseException("Error while trying to check profile %s existence: %s" % (name, ex))


    def add_profile(self, profile, conn):
        if self.profile_exists(profile.name, conn):
            raise DataException('Profile %s already exists' % profile.name)
        try:
            c = conn.cursor()
            c.execute(PROFILE_ADD_QUERY, (profile.name, 1))
            id = conn.insert_id()
        except Exception, ex:
            conn.rollback()
            raise DatabaseException("Error while trying to insert profile: %s" % ex)
        try:
            profile_params = [
                (id, "installer_url", profile.installer_url),
                (id, "network_settings", profile.network_settings),
                (id, "disk_settings", profile.disk_settings),
                (id, "packages", profile.packages),
                (id, "preinstall", profile.preinstall),
                (id, "postinstall", profile.postinstall)
            ]
            c.executemany(PROFILE_PARAMS_ADD_QUERY, profile_params)
        except Exception, ex:
            conn.rollback()
            raise DatabaseException("Error while trying to insert profile parameters: %s" % ex)
        repos = []
        if profile.repos:
            for repo in profile.repos:
                repos.append((id, repo['id']))
            try:
                c.executemany(PROFILE_ADD_REPOSITORY_BINDINGS, repos)
            except Exception, ex:
                conn.rollback()
                raise DatabaseException("Error while trying to insert profile repositories: %s" % ex)
        try:
            conn.commit()
            return id
        except Exception, ex:
            conn.rollback()
            raise DatabaseException("Error while trying to commit profile: %s" % ex)

    #STUB
    def update_profile(self, profile, conn):
        if not self.profile_exists(profile.name, conn):
            raise DataException("Profile %s does not exist" % profile.name)
        c = conn.cursor()
        prof = profile.to_dict()
        try:
            c.execute(PROFILE_NAME_UPDATE_QUERY, (prof['name'], prof['id']))
        except Exception, ex:
            conn.rollback()
            raise DatabaseException("Error while trying to update profile #%s's name: %s" % (prof['id'], ex))
        PARAMS = ["installer_url", "network_settings", "disk_settings", "packages", "preinstall", "postinstall"]
        for param in PARAMS:
            try:
                c.execute(PROFILE_PARAM_UPDATE_QUERY, (prof[param], profile.id, param))
            except Exception, ex:
                conn.rollback()
                raise DatabaseException("Error while trying to update parameter %s of profile %s: %s" % (param, profile.name, ex))
        try:
            c.execute(PROFILE_DROP_REPOSITORY_BINDINGS, (prof['id'],))
        except Exception, ex:
            conn.rollback()
            raise DatabaseException("Error while trying to drop profile #%s's repository bindings: %s" % (prof['id'], ex))
        rep_params = []
        for repo in prof['repos']:
            rep_params.append((prof['id'], repo['id']))
        try:
            c.executemany(PROFILE_ADD_REPOSITORY_BINDINGS, rep_params)
        except Exception, ex:
            conn.rollback()
            raise DatabaseException("Error while trying to add profile #%s's repository bindings: %s" % (prof['id'], ex))
        try:
            conn.commit()
            return True
        except Exception, ex:
            conn.rollback()
            raise DatabaseException("Error while trying to commit profile: %s" % ex)


    def get_profiles_list(self, conn):
        try:
            c = conn.cursor()
            c.execute(PROFILE_LIST_QUERY)
            profiles = c.fetchall()
            c.close()
        except Exception, ex:
            raise DatabaseException("Error while trying to get profile list: %s" % ex)
        result = []
        for profile in profiles:
            result.append({
                'name': profile[0],
                'status': profile[1]
            })
        return result

    #STUB
    def set_profile_status(self, name, status, conn):
        pass