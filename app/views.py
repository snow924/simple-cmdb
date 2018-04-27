# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,render,RequestContext,redirect
from django.http import HttpResponse,HttpRequest
from django.template import loader,Context
from django.core.paginator import EmptyPage,InvalidPage,Paginator,PageNotAnInteger
import MySQLdb
import MySQLdb.cursors
import os,re,commands 
import datetime
from models import Topic,ansible
from cmdb import models

try:
    import json
except ImportError:
    import simplejson as json
 
mysql_host = 'localhost'
mysql_db = 'ansible'
mysql_user = 'root'
mysql_pwd = ''

def DB_connect(sql):
'''
mysql数据库连接
'''
    conn = MySQLdb.connect(host=mysql_host,
                           user=mysql_user,
                           passwd=mysql_pwd,
                           db=mysql_db,
                           port=3306,
                           charset='utf8',
                           connect_timeout=2,
                           cursorclass=MySQLdb.cursors.DictCursor)
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()  
        return cursor.fetchall()
    except Exception, e:
        conn.rollback()  
        return "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
    conn.close()


def upload_file(request):
'''
上传文件前端页面
'''
    from django import forms
    class UploadFileForm(forms.Form):
        title = forms.CharField(max_length=1000000)
        file = forms.FileField()
    if request.method == "GET":
        data='get'
    if request.method == "POST":
        f = handle_uploaded_file(request.FILES['t_file'])
	print f
    return render_to_response('upload.html',context_instance=RequestContext(request))
    #return HttpResponse(data)


def handle_uploaded_file(f):
'''
上传处理页面
'''
    f_path='/data/upload/'+f.name
    with open(f_path, 'wb+') as info:
        print f.name,f_path
        for chunk in f.chunks():
            info.write(chunk)
    return f


def  test(request):
	return render_to_response('test1.html')


def  index(request):
	return render_to_response('index.html')


def  page_front(request):
	return render_to_response('page_front.html')


def  code(request):
'''
代码发布前端页面
'''
	slist=[]
	if request.method == 'POST':
		group=request.POST.get('group_id',None)
		print group
		sg = models.Server_Device.objects.filter(group=group)
		print sg
		for group in sg:
			slist.append(group.ip)
			print group.ip
		print slist
		sslist=json.dumps(slist)
		print type(slist)
		dict={"hosts":slist}
		print dict
		ret=json.dumps(dict)
		# return render_to_response('code.html', { 'slist': slist})
		return HttpResponse(ret)
	else:
		result = models.Server_Group.objects.all()
		return render_to_response('code.html',{'result': result})


def code_update(request):
'''
代码发布处理页面，用ansible命令做示例
'''
	print 'code update'
	iplist= request.POST.getlist("checkbox")
	hosts= ','.join(iplist)
	cmd="ansible "+hosts+" -a uptime"
	print cmd
	status,result=commands.getstatusoutput(cmd)
	html = "<html><body><pre>%s</pre></body>" % result
	return HttpResponse(html)


def  navi(request):
'''
首页左边导航栏
'''
	return render_to_response('navi.html')


def login(request):
'''
登陆页面示例
'''
	if request.method == 'POST':
		user=request.POST.get('login-name',None)
		pwd=request.POST.get('login-pass',None)
		if user== 'admin' and pwd == 'admin':
			request.session['is_login'] = {'user':user}
#			user_dict=request.session.get('is_login',None)
			return redirect('/index/')
			return HttpResponse("hi,%s" % user_dict)
		else:
			return HttpResponse("password is wrong!") 
	return render_to_response('login.html')


def login_require(func):
'''
登陆装饰器
'''
	def login(request):
	        user_dict=request.session.get('is_login',None)
	        if user_dict:
#	    		return HttpResponse("in session")
			return func(request)
	        else:
	                return redirect('/login/')
	return login


def my_pagination(request, queryset, display_amount=3, after_range_num = 5,bevor_range_num = 4):
'''
分页函数
'''
    #按参数分页
    paginator = Paginator(queryset, display_amount)
    try:
        #得到request中的page参数
        page =int(request.GET.get('page'))
    except:
        #默认为1
        page = 1
    try:
        #尝试获得分页列表
        objects = paginator.page(page)
    #如果页数不存在
    except EmptyPage:
        #获得最后一页
        objects = paginator.page(paginator.num_pages)
    #如果不是一个整数
    except:
        #获得第一页
        objects = paginator.page(1)
    #根据参数配置导航显示范围
    if page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:page+bevor_range_num]
    else:
        page_range = paginator.page_range[0:page+bevor_range_num]
    return objects,page_range


def paging(request):
'''
分页函数
'''
#	if request.method == 'POST':
#		keyword=request.REQUEST.get('mypassword')
#	else:
#		keyword=request.REQUEST.get('keyword')

        topics=Topic.objects.all
#        topics1=Topic.objects.filter(title=keyword)
#	topics,page_range=my_pagination(request,topics1)
        return render_to_response('page.html',locals(),context_instance=RequestContext(request))


def edit_config(request):
'''
配置文件编辑
'''
	if request.is_ajax():
	        if request.method == 'GET':
			f = open('/usr/local/nginx/conf/nginx.conf','r')
			data = f.read()
			return  HttpResponse(data)
	else:
		return render_to_response('edit_config.html',locals())


#    if request.is_ajax():
#        if request.method == 'POST':
#            data = request.POST['name']
#            try:
#                f = open('/data/www/a.txt','w')
#                f.write(data)
#                f.close()
#            except:
#                pass
#        if request.method == 'GET':
#            try:
#                f = open('/data/www/a.txt','r')
#                data = f.read()
#                f.close()
#            except:
#                pass
#    elif not request.is_ajax():
#        return render_to_response('edit_config.html',locals())
#    return  HttpResponse(data)


def play_book(request):
'''
执行指定路径里面的play-book
'''

#	user_dict=request.session.get('is_login',None)
#	if user_dict:
		
		list=[]
		file_list=os.listdir("/data/nfs")
		sql = 'select name from password'  
		result = DB_connect(sql)
		for result2 in result:
			list.append(result2['name'])
		return render_to_response('play_book.html',{'file_list':file_list,'result':list})
#	else:
#		return redirect('/login/')


def select(request):
'''
选择可执行的playbook文件
'''
		list=[]
#	if request.method == "POST":
		str=request.REQUEST.get('box1')
		method=request.method
		if request.REQUEST.get('box1') != "on":
			playbook_select=request.REQUEST.get('playbook_select')
        		cmd ="ansible-playbook /data/nfs/%s"  % playbook_select
        		status,result=commands.getstatusoutput(cmd)
       			html="<html><body><pre>%s</pre></body>" % result
        		return HttpResponse("execute sucess"    "%s" % html)
#			return render_to_response('select.html',{'select_result':str})
		else:
			playbook_select=request.REQUEST.get('playbook_select')
			my_passwd=request.REQUEST.get('mypassword')
			sql="select DECODE(password,'abracadabra') from password where name='%s'" % my_passwd
			select_result = DB_connect(sql)	
			for result2 in select_result:
                		list.append(result2["DECODE(password,'abracadabra')"])
			cmd ='ansible-playbook /data/nfs/%s --extra-vars ansible_ssh_pass="%s"' % (playbook_select,''.join(list))
        		status,result=commands.getstatusoutput(cmd) 
        		html="<html><body><pre>%s</pre></body>" % result
	      		return HttpResponse("execute sucess" 	"%s" % html)
#			return render_to_response('select.html',{'select_result':playbook_select})
#	else:
#		print "request.method is not post"


def  cmd(request):
'''
执行命令前端页面
'''
	return render_to_response('cmd.html')


def cmd_result(request):
'''
执行命令处理页面，尚未改成ajax当前页显示结果
'''
	if request.method == "POST":
		host=request.REQUEST.get('hostgroup')
		module=request.REQUEST.get('module')
		args=request.REQUEST.get('args')
	command="ansible %s -m %s -a '%s' " % (host,module,args)
	status,result=commands.getstatusoutput(command)
	html="<html><body><pre>%s</pre></body>" % result
	return HttpResponse("execute sucess"    "%s" % html)
	#return render_to_response('cn.html',{'host':host})


def index4(req,offset):
    offset=int(offset)
    next_time=datetime.datetime.now()+datetime.timedelta(hours=offset)
    return render_to_response("hours_ahead.html",{'hour_offset':offset,'next_time':next_time})


def index5(req):
    now=datetime.datetime.now()
    return render_to_response('current_datetime.html',{'current_date':now})
