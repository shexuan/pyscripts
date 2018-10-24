#!/usr/bin/env python3
# coding: utf-8


'''
Function: This scripts is to implement the linux comand scp while not need to
          enter passwd for every file.  
NOTE: the remote Directory must be existed, else exceptions.
'''


import paramiko
import os
import sys
import time
import argparse
import os


def ssh_scp_put(local_files,remote_files,ip,user,passwd,port='22'):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, 22, user, passwd)
    a = ssh.exec_command('date')
    stdin, stdout, stderr = a
    print(stdout.read())
    sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
    sftp = ssh.open_sftp()
    print(local_files)
    print(remote_files)
    sftp.put(local_files, remote_files)

def put():
    files = []
    if os.path.isdir(local_file):
        for root, dirs, files in os.walk(local_file):
            # root 当前目录的绝对路径
            # dirs 当前目录(root)下的文件夹
            # files 当前目录(root)下的文件
            for f in files:
                file_ = os.path.abspath(root+'/'+f)
                ssh_scp_put(file_,remote_dir+'/'+f,ip,user,passwd,port='22')
    else:
        file_name = os.path.basename(local_file)
        ssh_scp_put(local_file,remote_dir+'/'+file_name,ip,user,passwd,port='22')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="transfer file or dir between different computers.")
    parser.add_argument("--ip", "-i", type=str, help="IP-address")
    parser.add_argument("--user",'-u', type=str, help="username")
    parser.add_argument("-passwd", '-p', type=str, help='password')
    parser.add_argument("--local_file",'-lf',type=str,help="local file or directory to be copy transfered")
    parser.add_argument("--remote_dir",'-rd',type=str,help='remote saved directory')
    args = vars(parser.parse_args())

    ip = args["ip"]
    user = args["user"]
    passwd = args["passwd"]
    local_file = args["local_file"]
    remote_dir = args["remote_dir"]
    
    put()

