from django.db import models


class Topic(models.Model):
    title = models.CharField(max_length=200)
    name = models.CharField(max_length=10)

#    def __unicode__(self):
#        return self.name


class ansible(models.Model):
	ip_addr=models.CharField(max_length=50)
	hostgroup=models.CharField(max_length=50)
	username=models.CharField(max_length=50)
	passwd=models.CharField(max_length=50)
	
	def __unicode__(self):
		return self.ip_addr
