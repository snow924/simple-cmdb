#!/usr/bin/env python
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager

from ansible.plugins.callback import CallbackBase
import json

class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """
    
    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
      #  host = result._host
	print type(result._result)
        self.data = result._result
        #self.data = json.dumps(result._result)
        #self.data = json.dumps({host.name: result._result}, indent=4)

results_callback = ResultCallback()

Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection','module_path', 'forks', 'private_key_file', 'ssh_common_args', 'ssh_extra_args',
'sftp_extra_args', 'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check'])
variable_manager = VariableManager()
loader = DataLoader()

options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh', module_path=None, forks=100, private_key_file=None,
ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=False, become_method=None, become_user=None, verbosity=None, check=False)
passwords = {}

inventory = Inventory(loader=loader, variable_manager=variable_manager)
variable_manager.set_inventory(inventory)
play_source =  dict(
        name = "Ansible Play",
        hosts = 'localhost',
        gather_facts = 'no',
        tasks = [
            dict(action=dict(module='setup'))
         ]
  )
play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
qm = None
try:
    tqm = TaskQueueManager(
              inventory=inventory,
              variable_manager=variable_manager,
              loader=loader,
              options=options,
              passwords=passwords,
              stdout_callback=results_callback,
          )
    result = tqm.run(play)
    datastructure=results_callback.data
#    print type(datastructure)

    sn = datastructure['ansible_facts']['ansible_product_serial']
    host_name = datastructure['ansible_facts']['ansible_hostname']

    #description = datastructure['contacted'][ip]['ansible_facts']['ansible_lsb']['description']
    description = datastructure['ansible_facts']['ansible_env']['_system_name']
    ansible_machine = datastructure['ansible_facts']['ansible_machine']
    sysinfo = '%s %s' % (description, ansible_machine)

    os_kernel = datastructure['ansible_facts']['ansible_kernel']

    cpu = datastructure['ansible_facts']['ansible_processor'][1]
    cpu_count = datastructure['ansible_facts']['ansible_processor_count']
    cpu_cores = datastructure['ansible_facts']['ansible_processor_cores']
    mem = datastructure['ansible_facts']['ansible_memtotal_mb']

    ipadd_in = datastructure['ansible_facts']['ansible_all_ipv4_addresses'][0]
    disk = datastructure['ansible_facts']['ansible_devices']['sda']['size']
    
    data={}
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
#    print data
    import pprint
    pprint.pprint(data)


finally:
    if tqm is not None:
        tqm.cleanup()


