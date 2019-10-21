#!/usr/bin/python
 
from paramiko import SSHClient
import paramiko
import os
class SSH:
    def __init__(self):
        self.ssh = SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname='172.20.10.109',username='ubuntu',password='lucas123')
 
    def exec_cmd(self,cmd):
        print os.system(cmd)
        stdin,stdout,stderr = self.ssh.exec_command(cmd)
        if stderr.channel.recv_exit_status() != 0:
            print stderr.read()
        else:
            print stdout.read()
 
if __name__ == '__main__':
    ssh = SSH()
    ssh.exec_cmd("sudo microk8s.kubectl get pods")