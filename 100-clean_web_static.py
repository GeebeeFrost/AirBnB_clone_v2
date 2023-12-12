#!/usr/bin/python3
"""This module contains the do_clean function."""
import os
from fabric.api import env, lcd, local, run, cd

env.hosts = ['52.91.135.55', '54.173.96.139']


def do_clean(number=0):
    """Deletes out-of-date archives."""

    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    for i in range(number):
        archives.pop()
    with lcd("versions"):
        for archive in archives:
            local("rm ./{}".format(archive))

    with cd("/data/web_static/releases"):
        files = run("ls -tr").split()
        versions = [fl for fl in files if "web_static_" in fl]
        for i in range(number):
            versions.pop()
        for version in versions:
            run("rm -rf ./{}".format(version))
