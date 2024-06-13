from django.db import models
from public.models import *

# Create your models here.
class Attendence(models.Model):
    emid=models.ForeignKey(Register,on_delete=models.CASCADE,null=True)
    attendence=models.CharField(default="Leave",max_length=250)
    current_date = models.DateField(default=timezone.now) 
    current_time =models.DateTimeField(null=True)


class Salary(models.Model):
    eid=models.ForeignKey(Register,on_delete=models.CASCADE,null=True,related_name="eid")
    Salary=models.IntegerField(null=True)
    month=models.CharField(default='',max_length=250)
    current_date = models.DateField(default=timezone.now) 
   