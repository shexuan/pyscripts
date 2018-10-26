#!/usr/bin/env python3
# coding: utf-8


'''
Function: TO automatically input the password for linux command scp when transfer many files.  
NOTE: the remote Directory must be existed, else exceptions.
'''


import pexpect
import os
import sys
import time
import argparse
import os
"/bin/bash", ["-c", cmd]


def scpy(local_file, user, ip, passwd, remote, types):
    if types == 'file':
        recursive = ''
    if types == 'directory':
        recursive = '-r'
    cmd = "scp {recursive} {local_file} {user}@{ip}:{remote}".format(
        recursive=recursive, user=user, local_file=local_file, ip=ip, remote=remote)
    child = pexpect.spawn("/bin/bash", ["-c", cmd])
    child.expect(".*password:")
    child.sendline(passwd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="transfer file or dir between different computers.")
    parser.add_argument("--ip", "-i", type=str, help="IP-address")
    parser.add_argument("--user", '-u', type=str, help="username")
    parser.add_argument("-passwd", '-p', type=str, help='password')
    parser.add_argument("--local_file", '-lf', type=str, help="local file or directory to be copy transfered")
    parser.add_argument("--remote_dir", '-rd', type=str, help='remote saved directory')
    args = vars(parser.parse_args())

    ip = args["ip"]
    user = args["user"]
    passwd = args["passwd"]
    local_file = args["local_file"]
    remote_dir = args["remote_dir"]

    if not os.path.exists(local_file):
        raise SystemExit('FileNotFound: ', local_file)
    if os.path.isdir(local_file):
        types = 'directory'
    else:
        types = 'file'
    scpy(local_file, user, ip, passwd, remote_dir, types)
