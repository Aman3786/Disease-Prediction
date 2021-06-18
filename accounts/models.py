from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class DoctorInfo(models.Model):
    firstName = models.CharField(max_length=255)
    lastName  = models.CharField(max_length=255)
    username  = models.ForeignKey(User , on_delete=models.CASCADE)
    address   = models.CharField(max_length=500)
    clinic_name = models.CharField(max_length=256)
    specialization = models.CharField(max_length=255)
    phone  = models.IntegerField()
    description = models.TextField(max_length=500)
    image = models.CharField(max_length=150,null=True)
    
    def __str__(self):
        return self.firstName + self.lastName




# first name/last name / user forieng key /add clinic / speciallization / phone / image / description 

# Feed back / issue form 

