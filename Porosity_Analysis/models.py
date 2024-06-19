from django.db import models

class Porosity_register(models.Model):
    username = models.CharField(max_length=100,blank=True)
    designation = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    por_admin_lg = models.BooleanField(default=False)



class Porosity_data(models.Model):
    pressure_psi            =  models.CharField(max_length=100,blank=True)
    volume_mercury_intruded = models.CharField(max_length=100, blank=True)
    cumulative_volume = models.CharField(max_length=100, blank=True)
    pore_diameter_nm = models.CharField(max_length=100, blank=True)
    specific_surface_area = models.CharField(max_length=100, blank=True)
    avg_pore_size_nm = models.CharField(max_length=100, blank=True)
    median_pore_size_nm = models.CharField(max_length=100, blank=True)
    total_pore_volume = models.CharField(max_length=100, blank=True)
    tortuosity = models.CharField(max_length=100, blank=True)
    permeability_mDarcy = models.CharField(max_length=100, blank=True)
    adsorption_capacity = models.CharField(max_length=100, blank=True)
    client_id = models.CharField(max_length=100, blank=True)
