from django.db import models

# Create your models here.
class Post_image(models.Model):
    # pass
    image = models.ImageField(upload_to='disease_img/',null=True,blank=True)
    # tagi   = models.CharField(max_length=100,blank=True,null=True)
    # labels = models.CharField(max_length=100,blank=True,null=True)

    # def __str__(self):
    #     return str(self.tagi)

 
