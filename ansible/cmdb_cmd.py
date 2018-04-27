import commands
import json
import pprint

(status, output) = commands.getstatusoutput("ansible pc -m setup|sed '1c {'")
#print status, output

datastructure=json.loads(output)
print type(datastructure)

sn = datastructure['ansible_facts']['ansible_product_serial']
host_name = datastructure['ansible_facts']['ansible_hostname']

#description = datastructure['contacted'][ip]['ansible_facts']['ansible_lsb']['description']
#description = datastructure['ansible_facts']['ansible_env']['_system_name']
ansible_machine = datastructure['ansible_facts']['ansible_machine']
#sysinfo = '%s %s' % (description, ansible_machine)
#sysinfo = '%s' % (ansible_machine)

os_kernel = datastructure['ansible_facts']['ansible_kernel']

cpu = datastructure['ansible_facts']['ansible_processor'][1]
cpu_count = datastructure['ansible_facts']['ansible_processor_count']
cpu_cores = datastructure['ansible_facts']['ansible_processor_cores']
mem = datastructure['ansible_facts']['ansible_memtotal_mb']
os=datastructure['ansible_facts']['ansible_distribution']
ver=datastructure['ansible_facts']['ansible_distribution_version']
os_ver=os + ver
print os_ver

ip = datastructure['ansible_facts']['ansible_all_ipv4_addresses'][0]

mac=datastructure['ansible_facts']['ansible_default_ipv4']['macaddress']
#disk = datastructure['ansible_facts']['ansible_devices']['sda']['size']
disk = datastructure['ansible_facts']['ansible_devices']
#print  disk.keys()
d=[]
for key in disk.keys():
	disk = key+":"+datastructure['ansible_facts']['ansible_devices'][key]['size']
	d.append(disk)

data={}
data['sn'] = sn
#data['sysinfo'] = sysinfo
data['cpu'] = cpu
data['cpu_count'] = cpu_count
data['cpu_cores'] = cpu_cores
data['mem'] = mem
data['disk'] = unicode(d)
data['ip'] = ip
data['mac'] = mac
#data['os_kernel'] = os_kernel
data['host_name'] = host_name
data['os'] = os_ver
# print data
print type(sn)
pprint.pprint(data)
