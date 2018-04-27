#!/usr/bin/env python
# encoding: utf-8
import ansible.runner
aa = ansible.runner.Runner(
        module_name = 'shell',        
        module_args = 'uptime',    
        host_list = '/etc/ansible/hosts', 
        pattern = 'vmware',     
	remote_user='root',
	remote_pass='111111'
        )                     
bb = aa.run()
print bb
