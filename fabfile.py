# -*- coding: utf8 -*-
from fabric.context_managers import cd
from fabric.decorators import task
from fabric.operations import run, sudo
from fabric.state import env

env.hosts = ['web@lkng.me']

@task(default=True)
def deploy():
    code_dir = "/home/web/ulkng"
    with cd(code_dir):
        run("git pull origin master")
    sudo("touch /etc/uwsgi/apps-enabled/ulkng.ini")