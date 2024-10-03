from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    role = models.CharField(max_length=50,blank=True,null=True,default="admin")
    emp_id=models.CharField(max_length=15,null=True)  
    class Meta:
        db_table = 'auth_user'
    
class Person_Details(models.Model):
    name=models.CharField(max_length=100,null=True)  
    email=models.EmailField(null=True)  
    role=models.CharField(max_length=15,null=True)  
    emp_id=models.CharField(max_length=15,null=True)  
    ctc=models.CharField(max_length=50,null=True)  
    doj=models.DateField(null=True) 
    
class Salary(models.Model):
    name=models.CharField(max_length=100,null=True) 
    emp_id=models.CharField(max_length=15,null=True)       
    sal_id=models.ForeignKey(Person_Details,on_delete=models.CASCADE) 
    ctc=models.CharField(max_length=100,null=True)  
    month_ctc=models.CharField(max_length=100,null=True)  
    month=models.CharField(max_length=100,null=True)
    day_salary=models.CharField(max_length=100,null=True)
    present_days=models.CharField(max_length=100,null=True)
    status=models.CharField(max_length=100,null=True)
    net_salary=models.CharField(max_length=100,null=True)