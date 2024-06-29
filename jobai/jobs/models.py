from django.db import models

# Create your models here.
class Jobs(models.Model):
    jobname = models.CharField(max_length=300)
    jobdescription = models.CharField(max_length=1000,null=True)
    joburl = models.CharField(max_length=200,null=True)
    jobbenefit = models.CharField(max_length=1000,null=True)
    jobqualification = models.CharField(max_length=1000,null=True)
    jobskills = models.CharField(max_length=150,null=True)
    joblocation = models.CharField(max_length=100,null=True)
    jobtype = models.CharField(max_length=200,null=True)
    jobpostdate = models.DateTimeField(null=True)
    companyname = models.CharField(max_length=200,null=True)
    companydescription = models.CharField(max_length=1000,null=True)
    companyimage = models.CharField(max_length=200,null=True)