#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
from jinja2 import Template, Environment, PackageLoader
from my_exceptions import DatabaseException, DataException, InternalException

SERVER_ADD_QUERY = """insert into `servers` (`id`, `discover_date`, `mac`, `hostname`, `profile_id`) values (NULL, %s, %s, %s, %s)"""
SERVER_ADD_PARAMETER_QUERY = """insert into `server_parameters` (`id`, `server_id`, `name`, `value`) values (NULL, %s, %s, %s)"""
SERVER_ADD_INTERFACE_QUERY = """insert into `server_interfaces` (`id`, `server_id`, `name`, `status`, `mac`) values (NULL, %s, %s, %s, %s)"""
SERVER_ADD_REPOSITORY_BINDINGS = """insert into `servers_repositories` (`id`, `server_id`, `repo_id`) values (NULL, %s, %s)"""

SERVER_GET_BY_ID_QUERY = """select `servers`.`id`, `servers`.`discover_date`, `servers`.`mac`, `servers`.`hostname`,
                            `servers`.`profile_id`, `server_parameters`.`name`, `server_parameters`.`value`
                            from `servers`, `server_parameters` where `servers`.`id` = %s and
                            `servers`.`id` = `server_parameters`.`id`"""

SERVER_GET_BY_MAC_QUERY = """select `servers`.`id`, `servers`.`discover_date`, `servers`.`mac`, `servers`.`hostname`,
                             `servers`.`profile_id`, `server_parameters`.`name`, `server_parameters`.`value`
                             from `servers`, `server_parameters` where `servers`.`mac` = %s and
                             `servers`.`id` = `server_parameters`.`id`"""

SERVER_GET_BY_NAME_QUERY = """select `servers`.`id`, `servers`.`discover_date`, `servers`.`mac`, `servers`.`hostname`,
                              `servers`.`profile_id`, `server_parameters`.`name`, `server_parameters`.`value`
                              from `servers`, `server_parameters` where `servers`.`name` = %s and
                              `servers`.`id` = `server_parameters`.`id`"""

SERVER_GET_INTERFACES_QUERY = """select `servers`.`id`, `server_interfaces`.`name`, `server_interfaces`.`status`,
                                `server_interfaces`.`mac` from `servers`, `server_interfaces` where `servers`.`id` = %s
                                and `servers`.`id` = `server_interfaces`.`id`"""

SERVER_GET_REPOSITORIES_QUERY = """select `servers`.`id`, `repositories`.`name`, `repositories`.`url`, `repositories`.`id`
                                   from `servers`, `repositories`, `servers_repositories` where `servers`.`id` = %s and
                                   `servers`.`id` = `servers_repositories`.`server_id` and
                                   `repositories`.`id` = `servers_repositories`.`repo_id`"""

SERVER_UPDATE_QUERY = """update `servers` set `mac` = %s, `hostname` = %s, `profile_id` = %s where id = %s"""
SERVER_UPDATE_PARAMETER_QUERY = """update `servers` set `value` = %s where `server_id` = %s and `name` = %s"""

SERVER_DROP_REPOSITORY_BINDINGS = """delete from `servers_repositories` where `servers_repositories`.`server_id` = %s"""
SERVER_DROP_PARAMETERS_QUERY = """delete from `server_parameters` where `server_parameters`.`server_id` = %s"""
SERVER_DELETE_QUERY = """delete from `servers` where `id` = %s"""

SERVER_LIST_QUERY = """select `id`, `discover_date`, `mac`, `hostname`, `profile_id` from servers"""

class Server:
    def __init__(self, id=None, mac="", installer_url="", network_settings="", disk_settings="", repos=[], packages="",
                 interfaces=[], hostname="", ip="", netmask="", gw="", nameserver="", preinstall="", postinstall="",
                 info_cpu="", info_memory="", info_disks="", profile_id=0, discover_date=None):
        """

        @type info_disks: __builtin__.unicode
        """
        self.id = id
        self.mac = mac
        self.installer_url = installer_url
        self.network_settings = network_settings
        self.disk_settings = disk_settings
        self.repos = repos
        self.packages = packages
        self.interfaces = interfaces
        self.hostname = hostname
        self.ip = ip
        self.gw = gw
        self.nameserver = nameserver
        self.netmask = netmask
        self.preinstall = preinstall
        self.postinstall = postinstall
        self.info_cpu = info_cpu
        self.info_memory = info_memory
        self.info_disks = info_disks
        self.profile_id = profile_id
        self.discover_date = discover_date

    #FIXME: check interface order
    def determine_interface(self):
        result = None
        for iface in self.interfaces:
            if iface['status'] == 'UP':
                result = iface['name']
                break
        return result

    def format_mac_for_pxe(self):
        return self.mac.replace(':','-').lower()

    """
network --device {{ interface }} --hostname {{ hostname }} --bootproto static --ip={{ ip }} --netmask={{ mask }} --gateway={{ gateway }} --nameserver={{ nameserver }} --onboot=yes --mtu=1500
    """
    def to_kickstart(self):
        env = Environment(loader=PackageLoader('pattern', 'templates'))
        net_tmpl = env.from_string(self.network_settings)
        network = net_tmpl.render(interface=self.determine_interface(), ip=self.ip, mask=self.netmask, gateway=self.gw,
                                  nameserver=self.nameserver, hostname=self.hostname)
        env = Environment(loader=PackageLoader('pattern', 'templates'))
        tmpl = env.get_template('kickstart.cfg')
        return tmpl.render(url=self.installer_url, network=network, partitions=self.disk_settings,
                       repos=self.repos, packages=self.packages, preinstall=self.preinstall,
                       postinstall=self.postinstall)

    def to_pxe(self, baseurl):
        env = Environment(loader=PackageLoader('pattern', 'templates'))
        tmpl = env.get_template('pxelinux.tmpl')
        return {
            'config': tmpl.render(hostname=self.hostname, baseurl=baseurl, interface=self.determine_interface()),
            'name': "01-%s" % self.format_mac_for_pxe()
        }

    def to_dict(self):
        return {
            'id': self.id,
            'mac': self.mac,
            'installer_url': self.installer_url,
            'network_settings': self.network_settings,
            'disk_settings': self.disk_settings,
            'repos': self.repos,
            'packages': self.packages,
            'interfaces': self.interfaces,
            'hostname': self.hostname,
            'ip': self.ip,
            'gw': self.gw,
            'nameserver': self.nameserver,
            'netmask': self.netmask,
            'preinstall': self.preinstall,
            'postinstall': self.postinstall,
            'info_cpu': self.info_cpu,
            'info_memory': self.info_memory,
            'info_disks': self.info_disks,
            'profile_id': self.profile_id,
            'discover_date': self.discover_date
        }

class ServerManager:
    def __init__(self):
        pass

    def _get_server(self, param, value, conn):
        if param == 'id':
            q = SERVER_GET_BY_ID_QUERY
        elif param == 'mac':
            q = SERVER_GET_BY_MAC_QUERY
        elif param == 'name':
            q = SERVER_GET_BY_NAME_QUERY
        else:
            raise InternalException('Cannot get server by %s' % param)
        server_dict = {
            'id': None,
            'mac': None,
            'installer_url': None,
            'network_settings': None,
            'disk_settings': None,
            'repos': None,
            'packages': None,
            'interfaces': None,
            'hostname': None,
            'ip': None,
            'gw': None,
            'nameserver': None,
            'netmask': None,
            'preinstall': None,
            'postinstall': None,
            'info_cpu': None,
            'info_memory': None,
            'info_disks': None,
            'discover_date': None,
            'profile_id': None
        }

        """
        Get server parameters
        """
        try:
            c = conn.cursor()
            c.execute(q, (value,))
        except Exception ,ex:
            raise DatabaseException("Could not get server parameters by %s=%s: %s", (param, value, ex))
        for arr in c:
            server_dict['id'] = arr[0]
            server_dict['discover_date'] = arr[1]
            server_dict['mac'] = arr[2]
            server_dict['hostname'] = arr[3]
            server_dict['profile_id'] = arr[4]
            if arr['5'] in server_dict:
                server_dict[arr[5]] = arr[6]
        """
        Get server interfaces
        """
        try:
            c = conn.cursor()
            c.execute(SERVER_GET_INTERFACES_QUERY, (server_dict['id'],))
        except Exception ,ex:
            raise DatabaseException("Could not get server interfaces by id=%s: %s", (server_dict['id'], ex))
        server_dict['interfaces'] = []
        for iface in c:
            server_dict['interfaces'].append({
                'name': iface[1],
                'status': iface[2],
                'mac': iface[3]
            })
        """
        Get server repositories
        """
        try:
            c = conn.cursor()
            c.execute(SERVER_GET_REPOSITORIES_QUERY (server_dict['id'],))
        except Exception ,ex:
            raise DatabaseException("Could not get server repositories by id=%s: %s", (server_dict['id'], ex))
        server_dict['repos'] = []
        for repo in c:
            server_dict['repos'].append({
                'name': repo[1],
                'url': repo[2],
                'id': repo[3]
            })
        return Server(**server_dict)

    def get_server_by_id(self, id, conn):
        return self._get_server('id', id, conn)

    def get_server_by_mac(self, mac, conn):
        return self._get_server('mac', mac, conn)

    def get_server_by_name(self, name, conn):
        return self._get_server('name', name, conn)

    def add_server(self, server, conn):
        pass

    def update_server(self, server, conn):
        pass

    def delete_server(self, id, conn):
        pass

    def get_servers_list(self, conn):
        pass

