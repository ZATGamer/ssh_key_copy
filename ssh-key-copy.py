#!/bin/python
import csv
import config
from fabric.api import *


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
    ssh_key_path = '.ssh/idrsa'
    localpath = './remote_keys/'
    run('echo -e "\n\n\n" | ssh-keygen -t rsa -f {}'.format(ssh_key_path))
    get(ssh_key_path, localpath + "." + env.host)



# Copy pub keys here and add them to the key's list


def generate_key_file(pub_keys):
    # Generate the authorized_keys file
    with open('authorized_keys', 'w') as key_file:
        for key in pub_keys:
            key_file.write(key)

# Copy authorized_keys back out to the servers






if __name__ == '__main__':
    hosts = []
    pub_keys = []

    env.user = config.ssh['user']
    env.key_filename = config.ssh['ssh_key']
    env.parallel = True


    read_hosts(hosts)
    env.hosts = hosts



    read_key(pub_keys, 'default_keys')

    generate_key_file(pub_keys)