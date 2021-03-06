#!/bin/python

import csv
import config
from fabric.api import *
import os


def read_hosts(hosts):
    # Read in host names from file
    with open('hostlist.txt') as hostfile:
        hostfile = csv.reader(hostfile)
        for row in hostfile:
            hosts.append(row[0])


def read_key(pub_keys, new_keys):
    # Read in standard SSH keys everyone gets
    with open(new_keys) as keyfile:
        for row in keyfile:
            pub_keys.append(row)


def get_keys():
    # Go to each host and generate a key
    user = config.ssh['user']
    ssh_key_path = '/home/{}/.ssh/id_rsa'.format(user)
    ssh_pubkey_path = '/home/{}/.ssh/id_rsa.pub'.format(user)
    localpath = './remote_keys/id_rsa.pub'
    run("ssh-keygen -f {} -t rsa -N ''".format(ssh_key_path))
    # Copy pub keys here.
    get(ssh_pubkey_path, localpath + "." + env.host)


def generate_key_file(pub_keys):
    # Generate the authorized_keys file
    with open('authorized_keys', 'w') as key_file:
        for key in pub_keys:
            key_file.write(key)


def copy_auth_keys_to_server():
    # Copy authorized_keys back out to the servers
    user = config.ssh['user']
    remote_auth_key_location = '/home/{}/.ssh/authorized_keys'.format(user)
    put('./authorized_keys', remote_auth_key_location)
    run('chmod 600 {}'.format(remote_auth_key_location))


def clean_up():
    # Clean up local drive
    os.remove('./authorized_keys')
    for file in os.listdir('remote_keys'):
        os.remove('./remote_keys/{}'.format(file))
    os.rmdir('./remote_keys')


if __name__ == '__main__':
    # List defining
    hosts = []
    pub_keys = []

    # Fabric config
    env.user = config.ssh['user']
    env.key_filename = config.ssh['ssh_key']
    env.parallel = True

    read_hosts(hosts)
    for host in hosts:
        # read hosts from file into fabric hosts list
        env.hosts.append(host)

    read_key(pub_keys, 'default_keys')

    # Fabric execution
    execute(get_keys)

    for file in os.listdir('remote_keys'):
        # Add keys to key list
        remote_key_local = './remote_keys/{}'.format(file)
        read_key(pub_keys, remote_key_local)

    generate_key_file(pub_keys)

    # Fabric execution
    execute(copy_auth_keys_to_server)

    clean_up()


