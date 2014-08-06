from paramiko import SSHClient, SSHConfig
import os
#setup config
config = SSHConfig()
abs_path = ('/Users/sabina/.ssh/config')
base_path = os.path.dirname(__file__)
rel_path = os.path.relpath(abs_path)
new_path = (os.path.join(base_path,rel_path))
config.parse(open(new_path,'r'))
o = config.lookup('we')
#get into aws 
ssh_client = SSHClient()
ssh_client.load_system_host_keys()
print o.keys()
ssh_client.connect(o['hostname'], username=o['user'], key_filename=o['identityfile'])
cmds=['pwd','ls','cd oakpark']

#stdin, stdout, stderr = ssh_client.exec_command(cmds[2])
#ssh_client.exec_command(cmds[2])
sftp = ssh_client.open_sftp()
print sftp.getcwd()
#lines = []
#for l in stdout:
#    lines.append(l)
#print str(lines[1])

f =  sftp.listdir('oakpark/')
print type(f)
files = [] 

for l in f:
    files.append(f)

print files[0][0]
print 'oakpark/{}'.format(str(files[0]))
file = sftp.open('oakpark/{}'.format(str(files[0][0])))


