from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.db import models
from django.utils import timezone



class Departments(models.Model):
    departmentname = models.CharField(max_length=50,default='')
    def __str__(self):
        return self.departmentname
# Create your models here.
class Register(AbstractUser):
    name = models.CharField(max_length=50,null=True,unique=True)
    contact = models.IntegerField(null=True,unique=True)
    usertype = models.IntegerField(null=True)
    status = models.IntegerField(default=0)
    role = models.CharField(null=True,max_length=100)
    registrationid=models.IntegerField(null=True,unique=True)
    Department= models.ForeignKey(Departments,on_delete=models.CASCADE,null=True)
    salary=models.IntegerField(null=True,default=0)    

    def __str__(self):
        return self.name
class UploadFile(models.Model):
    file = models.FileField()
    def __str__(self) -> str:
        return self.file.name   
class Projects(models.Model):
    title = models.CharField(max_length=50, null=True)
    description = models.TextField(null=True)
    start_date = models.DateField(null=True)
    due_date = models.DateField(null=True)
    current_date = models.DateField(default=timezone.now)
    file = models.FileField(blank=True)    
class Task(models.Model):
    title = models.CharField(max_length=50,null=True)
    description = models.TextField(null=True)
    start_date = models.DateField(null=True)
    due_date = models.DateField(null=True)
    current_date = models.DateField(default=timezone.now) 
    project = models.ForeignKey(Projects,on_delete=models.CASCADE,null=True)
    assigned_staff = models.ForeignKey(Register,on_delete=models.CASCADE,null=True,related_name='+')
    file = models.FileField(null=True) 
    status = models.CharField(null=True,default="Not updated",max_length=250)
    
class timesheet(models.Model):
    task=models.ForeignKey(Task,on_delete=models.CASCADE,null=True)
    workinghours=models.IntegerField(null=True)
    assigned_staff = models.ForeignKey(Register,on_delete=models.CASCADE,null=True,related_name='+')
    current_date = models.DateField(default=timezone.now) 
    current_time =models.DateTimeField(default=timezone.now)

class complaints(models.Model):
    userid = models.ForeignKey(Register,on_delete=models.CASCADE,null=True,related_name='+')
    title = models.CharField(max_length=50,null=True)
    description = models.TextField(null=True)
    file = models.FileField(blank=True)
    response=models.CharField(max_length=50,null=True)
    current_date = models.DateField(default=timezone.now) 
    status=models.IntegerField(null=True,default=0)
LTYPE_CHOICES = [
    ('', 'Select'),
    ('Full Day', 'Full Day'),
    ('Half Day', 'Half Day'),
]
class leave(models.Model):
    userid = models.ForeignKey(Register,on_delete=models.CASCADE,null=True,related_name='+')
    reason=models.CharField(max_length=50,null=True)
    date=models.DateField(null=True)
    ltype=models.CharField(max_length=50,null=True,choices=LTYPE_CHOICES)
    current_date = models.DateField(default=timezone.now) 
    status=models.IntegerField(null=True,default=0)    





        

        
    


    


