from django.db import models



class Client_register(models.Model):
    username = models.CharField(max_length=100,blank=True)
    location = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    consumer_id = models.CharField(max_length=100,unique=True,null=True)
    cl_admin_lg = models.BooleanField(default=False)





class Client_orders(models.Model):
    consumer_id = models.CharField(max_length=15,null=True)
    username    = models.CharField(max_length=100, blank=True)
    email       = models.EmailField()
    product     = models.CharField(max_length=50)
    quantity    = models.IntegerField()

    manganese_Comp = models.CharField(max_length=100, null=True, default=None)
    manganese_form = models.CharField(max_length=100, null=True, default=None)
    manganese_size = models.CharField(max_length=100, null=True, default=None)
    manganese_mass = models.CharField(max_length=100, null=True, default=None)

    mang_admin_approve = models.BooleanField(default=False)

    # Component Processing at App Integration
    app_process = models.BooleanField(default=False)
    app_admin_approve = models.BooleanField(default=False)
    material_volume   = models.CharField(max_length=100, null=True, default=None)

    fin_porosity_value = models.BooleanField(default=False)
    porsity_value = models.CharField(max_length=100, null=True, default=None)
    mercury_intuduced  = models.CharField(max_length=100, null=True, default=None)

    prediction = models.CharField(max_length=100, null=True, default=None)
    porosity_result = models.CharField(max_length=100, null=True, default=None)
    porosity_fin_report = models.BooleanField(default=False)


    por_rep_admin_approve = models.BooleanField(default=False)
    por_rep_admin_reject = models.BooleanField(default=False)

    client_payment = models.BooleanField(default=False)
    amount = models.CharField(max_length=100, null=True, default=None)
    dispatch = models.BooleanField(default=False)

    porosity_test = models.BooleanField(default=False)
    maxi    = models.CharField(max_length=100, null=True, default=None)
    mercury = models.CharField(max_length=100, null=True, default=None)
    porosity_upload  = models.BooleanField(default=False)
    fintest=models.BooleanField(default=False, null=True)

    res= models.CharField(max_length=100, null=True, default=None)
    graph = models.FileField(upload_to='media/', null=True)
    report_pdf = models.FileField(upload_to='media/', null=True,max_length=5000)
    retest = models.BooleanField(default=True, null=True)
