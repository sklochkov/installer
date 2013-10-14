#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
import config
import json
from installer_server import InstallerServer
import logging
import traceback
CONFIG = "/etc/installer/installer.conf"


class InstallerServerApp(flask.Flask):
    def __init__(self, *args, **kwargs):
        self.cfg = config.parse(CONFIG)
        super(InstallerServerApp, self).__init__(*args, **kwargs)


app = InstallerServerApp(__name__)


@app.route('/discover/ping')
def ping():
    return "pong"


@app.route('/discover/api/info', methods=['POST'])
def accept_info():
    inssrv = InstallerServer(app.cfg['mysql']['host'][0], app.cfg['mysql']['user'][0], app.cfg['mysql']['password'][0],
                             app.cfg['mysql']['database'][0])
    if 'info' not in flask.request.form:
        flask.abort(400)
    info_raw = flask.request.form['info']
    try:
        info = json.loads(flask.request.form['info'])
    except:
        flask.abort(400)
    try:
        inssrv.accept_server_info(info)
    except:
        flask.abort(500)
    return "Not implemented"


@app.route('/discover/config/')
def configuration():
    try:
        inssrv = InstallerServer(app.cfg['mysql']['host'][0], app.cfg['mysql']['user'][0], app.cfg['mysql']['password'][0],
                             app.cfg['mysql']['database'][0])
        repos = inssrv.get_repo_list()
        profiles = inssrv.get_profiles_list()
        incl = flask.render_template('scripts_and_styles.html')
        hdr = flask.render_template('header.html')
        ftr = flask.render_template('footer.html')
        page = flask.render_template('configuration.html', includes=incl, header=hdr, footer=ftr, profiles=profiles, repos=repos)
        return page
    except Exception, ex:
        return traceback.format_exc()

@app.route('/discover/profiles')
def profiles_list():
    return "Not implemented yet"

@app.route('/discover/repo_add', methods=['POST'])
def add_repository():
    try:
        if 'repo_name' not in flask.request.form:
            flask.abort(400)
        if 'repo_url' not in flask.request.form:
            flask.abort(400)
        name = flask.request.form['repo_name']
        url = flask.request.form['repo_url']
        inssrv = InstallerServer(app.cfg['mysql']['host'][0], app.cfg['mysql']['user'][0], app.cfg['mysql']['password'][0],
                                 app.cfg['mysql']['database'][0])
        inssrv.add_repo(name, url)
        return flask.redirect('/discover/config/#repos')
    except Exception, ex:
        return traceback.format_exc()

@app.route('/discover/repo_edit')
def edit_repository():
    try:
        if 'repo_name' not in flask.request.form:
            flask.abort(400)
        if 'repo_url' not in flask.request.form:
            flask.abort(400)
        if 'repo_id' not in flask.request.form:
            flask.abort(400)
        name = flask.request.form['repo_name']
        url = flask.request.form['repo_url']
        id = flask.request.form['repo_id']
        inssrv = InstallerServer(app.cfg['mysql']['host'][0], app.cfg['mysql']['user'][0], app.cfg['mysql']['password'][0],
                                 app.cfg['mysql']['database'][0])
        inssrv.update_repo(id, name, url)
        return flask.redirect('/discover/config/#repos')
    except Exception, ex:
        return traceback.format_exc()

@app.route('/discover/repo_delete')
def delete_repository():
    try:
        if 'repo_id' not in flask.request.form:
            flask.abort(400)
        id = flask.request.form['repo_id']
        inssrv = InstallerServer(app.cfg['mysql']['host'][0], app.cfg['mysql']['user'][0], app.cfg['mysql']['password'][0],
                                 app.cfg['mysql']['database'][0])
        #assert isinstance(id, object)
        inssrv.delete_repo(id)
        return flask.redirect('/discover/config/#repos')
    except Exception, ex:
        return traceback.format_exc()

@app.route('/discover/repo_add_form', methods=['GET'])
def repo_form():
    try:
        id = flask.request.args.get('id')
        name = ""
        url = ""
        if id:
            inssrv = InstallerServer(app.cfg['mysql']['host'][0], app.cfg['mysql']['user'][0], app.cfg['mysql']['password'][0],
                             app.cfg['mysql']['database'][0])
            repo = inssrv.get_repo_by_id(id)
            name = repo['name']
            url = repo['url']
        incl = flask.render_template('scripts_and_styles.html')
        hdr = flask.render_template('header.html')
        ftr = flask.render_template('footer.html')
        return flask.render_template('repo_add.html', includes=incl, header=hdr, footer=ftr, name=name, url=url, action="add", id="")
    except Exception, ex:
        return traceback.format_exc()

@app.route('/discover/repo_edit_form', methods=['GET'])
def repo_form():
    try:
        id = flask.request.args.get('id')
        name = ""
        url = ""
        if id:
            inssrv = InstallerServer(app.cfg['mysql']['host'][0], app.cfg['mysql']['user'][0], app.cfg['mysql']['password'][0],
                             app.cfg['mysql']['database'][0])
            repo = inssrv.get_repo_by_id(id)
            name = repo['name']
            url = repo['url']
            id = repo['id']
        incl = flask.render_template('scripts_and_styles.html')
        hdr = flask.render_template('header.html')
        ftr = flask.render_template('footer.html')
        return flask.render_template('repo_add.html', includes=incl, header=hdr, footer=ftr, name=name, url=url, action="edit", id=id)
    except Exception, ex:
        return traceback.format_exc()