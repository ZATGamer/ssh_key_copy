# ssh_key_copy

This is a Quick and dirty script to enable ssh between servers.

It will:

- Read default_keys into a key_list.
- Generate SSH Key pair on remote servers
- Copy the id_rsa.pub from remote servers to the local drive from each server.
- Read all new pub keys into key_list
- Generate a authorized_keys from all keys in key_list
- Copy authorized_keys file to each remote server
- Change permissions of authorized_keys to 600
- Clean up local files.

# Requirements
- fabric