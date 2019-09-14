from paramiko import SSHClient
import paramiko
 
class ServerSSH:
    def __init__(self):
        self.ssh = SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname='10.42.0.193',username='ubuntu',password='lucas123')
 
    def exec_cmd(self,cmd):
        stdin,stdout,stderr = self.ssh.exec_command(cmd)
        if stderr.channel.recv_exit_status() != 0:
            return stderr.read()
        else:
            return stdout.read()
 
# if __name__ == '__main__':
#     ssh = SSH()
#     ssh.exec_cmd("ls")
    