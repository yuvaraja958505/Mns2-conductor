from django.db import models



class Manganese_register(models.Model):
    username = models.CharField(max_length=100,blank=True)
    designation = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    mg_admin_lg = models.BooleanField(default=False)




class Components_required(models.Model):
    component  = models.CharField(max_length=50,null=True)
    material   = models.CharField(max_length=50,null=True)
    product    = models.CharField(max_length=50,null=True)






