#!/usr/bin/python3
"""This module contains the deploy function"""
from datetime import datetime
from fabric.api import local, env, put, run
from os.path import isdir, isfile

env.hosts = ['52.91.135.55', '54.173.96.139']


def deploy():
    """Create and distribute an archive to web servers"""
    archive = do_pack()
    if not archive:
        print("Error creating archive.")
        return False
    return do_deploy(archive)


def do_pack():
    """Generates a tgz archive from the contents of web_static folder"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir('versions') is False:
            local("mkdir versions")
        filename = "versions/web_static_{}.tgz".format(date)
        print("Packing web_static to {}".format(filename))
        local("tar -cvzf {} web_static".format(filename))
        return filename
    except Exception:
        return None


def do_deploy(archive_path):
    """Distributes an archive to web servers"""
    if isfile(archive_path) is False:
        return False
    fwext = archive_path.split('/')[-1]
    fwoext = fwext.split('.')[0]

    if put(archive_path, "/tmp/").failed is True:
        print("Unable to upload archive to server\n")
        return False
    if (run("mkdir -p /data/web_static/releases/{}".format(fwoext)).failed
            is True):
        print("Unable to create directory on server\n")
        return False
    if (run("tar -xzf /tmp/{} -C /data/web_static/releases/{}".
            format(fwext, fwoext)).failed is True):
        print("Unable to extract archive on server\n")
        return False
    if run("rm /tmp/{}".format(fwext)).failed is True:
        print("Unable to delete archive from server\n")
        return False
    if (run("mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}".format(fwoext, fwoext)).failed
            is True):
        print("Unable to move archive contents to serve directory\n")
        return False
    if (run("rm -rf /data/web_static/releases/{}/web_static".
            format(fwoext)).failed is True):
        print("Unable to delete unnecessary empty folder\n")
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        print("Unable to delete existing symbolic link\n")
        return False
    if (run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
            format(fwoext)).failed is True):
        print("Unable to create symbolic link to new release\n")
        return False
    print("New version deployed successfully!\n")
    return True
