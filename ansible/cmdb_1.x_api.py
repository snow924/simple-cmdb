# -*- coding: UTF-8 -*-

import ansible.runner

def get_info(ip):
    data = {}
    runner = ansible.runner.Runner(module_name='setup', module_args='', pattern='all', forks=2)
    datastructure = runner.run()
    #print datastructure
    sn = datastructure['contacted'][ip]['ansible_facts']['ansible_product_serial']
    host_name = datastructure['contacted'][ip]['ansible_facts']['ansible_hostname']

    #description = datastructure['contacted'][ip]['ansible_facts']['ansible_lsb']['description']
    description = datastructure['contacted'][ip]['ansible_facts']['ansible_env']['_system_name']
    ansible_machine = datastructure['contacted'][ip]['ansible_facts']['ansible_machine']
    sysinfo = '%s %s' % (description, ansible_machine)

    os_kernel = datastructure['contacted'][ip]['ansible_facts']['ansible_kernel']

    cpu = datastructure['contacted'][ip]['ansible_facts']['ansible_processor'][1]
    cpu_count = datastructure['contacted'][ip]['ansible_facts']['ansible_processor_count']
    cpu_cores = datastructure['contacted'][ip]['ansible_facts']['ansible_processor_cores']
    mem = datastructure['contacted'][ip]['ansible_facts']['ansible_memtotal_mb']

    ipadd_in = datastructure['contacted'][ip]['ansible_facts']['ansible_all_ipv4_addresses'][0]
    disk = datastructure['contacted'][ip]['ansible_facts']['ansible_devices']['sda']['size']
    # print sysinfo
    data['sn'] = sn
    data['sysinfo'] = sysinfo
    data['cpu'] = cpu
    data['cpu_count'] = cpu_count
    data['cpu_cores'] = cpu_cores
    data['mem'] = mem
    data['disk'] = disk
    data['ipadd_in'] = ipadd_in
    data['os_kernel'] = os_kernel
    data['host_name'] = host_name

    print data

if __name__ == '__main__':
    data = get_info('10.10.1.128')

  #  import pprint
   # pprint.pprint(data)
