# coding=utf8
#from cmdb.models import Server_Device as Server_Device
from django.http import HttpResponse
from django.shortcuts import render_to_response,render,RequestContext,redirect

from cmdb import models

import commands
import json
import pprint
import math

def get_info(ip):
	cmd = "ansible "+ip+" -m setup|sed '1c {'"
#	print cmd
	(status, output) = commands.getstatusoutput(cmd)
#	print status, output
	
	datastructure=json.loads(output)
	print type(datastructure)
	
	sn = datastructure['ansible_facts']['ansible_product_serial']
	host_name = datastructure['ansible_facts']['ansible_hostname']
	print host_name
	
	#description = datastructure['contacted'][ip]['ansible_facts']['ansible_lsb']['description']
	#description = datastructure['ansible_facts']['ansible_env']['_system_name']
	ansible_machine = datastructure['ansible_facts']['ansible_machine']
	#sysinfo = '%s %s' % (description, ansible_machine)
	#sysinfo = '%s' % (ansible_machine)
	
#	os_kernel = datastructure['ansible_facts']['ansible_kernel']
	
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
	data['mem'] = round(int(mem)/1024.0)
	data['disk'] = '; '.join(d)
	data['ip'] = ip
	data['mac'] = mac
	#data['os_kernel'] = os_kernel
	data['hostname'] = host_name
	data['os'] = os_ver
	# print data
	print type(sn)
	pprint.pprint(data)
	return data


def postinfo(request):
	dic=get_info('10.36.40.43')
	print  "postinfo method", dic

	models.Server_Device.objects.create(**dic)
	return HttpResponse("post sucess")

def list(request):
	# result = models.Server_Device.objects.select_related('server_group').all()
	result = models.Server_Device.objects.all()
	print result
	for data in result:
		print data
	return render_to_response('list.html',{'result':result})

def show(request):
	# result = models.Server_Device.objects.select_related('idc').all()
	result = models.Server_Device.objects.all()
	print result
	for data in result:
		print data
	return render_to_response('show.html',{'result':result})

def update(request):
    # 提交服务器信息
    response = HttpResponse()
#    data = json.loads(request.GET.get('data', ''))
  #  print  request.POST.get
    print  request.POST.get('id')
    sid =  request.POST.get('id')
    id = int(sid)
    print 'update id --->',id
    server= models.Server_Device.objects.get(pk=id)
    print 'haha'
    print server.ip
    data = get_info(server.ip)
#    data = get_info('10.36.40.162')
#    server.os_version = data['sysinfo']
    server.hostname = data['hostname']
#    server.os_kernel = data['os_kernel']
    server.cpu = data['cpu']
    server.cpu_count = data['cpu_count']
    server.cpu_cores = data['cpu_cores']
    server.mem = data['mem']
    server.disk = data['disk']
    print "save before"
    print type(server)
    server.save()

    response.write(json.dumps(u'成功'))
    return HttpResponse ("update")


def project_list(request):
	result = models.Project.objects.all()
	return render_to_response('project_list.html',{'result':result})

def idc_list(request):
	result = models.IDC.objects.all()
	return render_to_response('idc_list.html',{'result':result})
