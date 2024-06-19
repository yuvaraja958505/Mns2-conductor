from django.db import models

class Application_register(models.Model):
    username = models.CharField(max_length=100,blank=True)
    designation = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    app_admin_lg = models.BooleanField(default=False)




