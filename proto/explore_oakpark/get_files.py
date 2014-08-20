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

sftp = ssh_client.open_sftp()

def get():
    f =  sftp.listdir('oakpark/non-duplicates/xml/')
    print type(f)
    files = [] 
    read_files=[]
    for l in f:
        # print l
        fil = (sftp.open('oakpark/non-duplicates/xml/{}'.format(str(l))))
        files.append(fil)
        read_files.append(fil.read())

    return files,read_files
