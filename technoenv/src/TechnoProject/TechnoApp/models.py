from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.utils.timezone import localtime

TEHCNO_USER_PERMISSIONS = [
    ('STORE', 'STORE'),
    ('PRODUCTION', 'PRODUCTION'),
    ('ADMIN','ADMIN')
]

TECHNO_ALLOY_CLASS = [
    ('PIPE','PIPE'),
    ('MGO','MGO'),
    ('CONDUCTOR','CONDUCTOR')
]

COIL_STATUS_CLASS = [
    ('ANNEALING','ANNEALING'),
    ('DRAW','DRAW')
]

# Create your models here.
class TechnoUser(User):

    user_type = models.CharField(
        max_length=10,
        choices=TEHCNO_USER_PERMISSIONS,
    )
    def save(self, *args, **kwargs):
        if self.pk == None:
            self.set_password(self.password)
        super(TechnoUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "TechnoUser"
        verbose_name_plural = "TechnoUsers"


class ElementMaster(models.Model):
    metal_code = models.CharField(max_length=10,primary_key=True)

class AlloyMaster(models.Model):
    alloy_name = models.TextField(blank=True,primary_key=True)
    alloy_class = models.CharField(
        max_length=10,
        choices=TECHNO_ALLOY_CLASS,
    )

class PipeAlloyElementMappingMaster(models.Model):
    alloy_obj = models.ForeignKey(AlloyMaster,on_delete=models.CASCADE)
    element_obj = models.ForeignKey(ElementMaster,on_delete=models.CASCADE)
    min_percent = models.DecimalField(max_digits=10, decimal_places=5)
    max_percent = models.DecimalField(max_digits=10, decimal_places=5)
    class Meta:
        unique_together = (('alloy_obj', 'element_obj'),)

class Pipe(models.Model):
    lot_number = models.TextField(primary_key=True, blank=True)
    qty = models.IntegerField()
    supplier_name = models.TextField(blank=True,null=True)
    alloy_obj = models.ForeignKey(AlloyMaster,on_delete=models.CASCADE)
    diameter = models.DecimalField(max_digits=10, decimal_places=5)        

class PipeAlloyElementQuantity(models.Model):
    pipe_obj = models.ForeignKey(Pipe,on_delete=models.CASCADE)
    element_obj = models.ForeignKey(ElementMaster,on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=5)
    class Meta:
        unique_together = (('pipe_obj', 'element_obj'),)

class ConductorAlloyElementMappingMaster(models.Model):
    alloy_obj = models.ForeignKey(AlloyMaster,on_delete=models.CASCADE)
    element_obj = models.ForeignKey(ElementMaster,on_delete=models.CASCADE)
    positive_min_percent = models.DecimalField(max_digits=10, decimal_places=5)
    positive_max_percent = models.DecimalField(max_digits=10, decimal_places=5)
    negative_min_percent = models.DecimalField(max_digits=10, null=True, blank=True, decimal_places=5)
    negative_max_percent = models.DecimalField(max_digits=10, null=True, blank=True, decimal_places=5)
    class Meta:
        unique_together = (('alloy_obj', 'element_obj'),)

class Conductor(models.Model):
    lot_number = models.TextField(primary_key=True, blank=True)
    qty = models.DecimalField(max_digits=15, decimal_places=5)
    supplier_name = models.TextField(blank=True,null=True)
    alloy_obj = models.ForeignKey(AlloyMaster,on_delete=models.CASCADE)
    diameter = models.DecimalField(max_digits=10, decimal_places=5)        

class ConductorAlloyElementQuantity(models.Model):
    conductor_obj = models.ForeignKey(Conductor,on_delete=models.CASCADE)
    element_obj = models.ForeignKey(ElementMaster,on_delete=models.CASCADE)
    positive_quantity = models.DecimalField(max_digits=10, decimal_places=5)
    negative_quantity = models.DecimalField(max_digits=10, null=True, blank=True, decimal_places=5)
    class Meta:
        unique_together = (('conductor_obj', 'element_obj'),)

class MGOAlloyElementMappingMaster(models.Model):
    alloy_obj = models.ForeignKey(AlloyMaster,on_delete=models.CASCADE)
    element_obj = models.ForeignKey(ElementMaster,on_delete=models.CASCADE)
    min_percent = models.DecimalField(max_digits=10, decimal_places=5)
    max_percent = models.DecimalField(max_digits=10, decimal_places=5)
    class Meta:
        unique_together = (('alloy_obj', 'element_obj'),)

class MGO(models.Model):
    lot_number = models.TextField(primary_key=True, blank=True)
    qty = models.DecimalField(max_digits=15, decimal_places=5)
    supplier_name = models.TextField(blank=True,null=True)
    alloy_obj = models.ForeignKey(AlloyMaster,on_delete=models.CASCADE)        

class MGOAlloyElementQuantity(models.Model):
    mgo_obj = models.ForeignKey(MGO,on_delete=models.CASCADE)
    element_obj = models.ForeignKey(ElementMaster,on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=5)
    class Meta:
        unique_together = (('mgo_obj', 'element_obj'),)

class ItemMaster(models.Model):
    item_code = models.TextField(blank=True,primary_key=True)        

class Coil(models.Model):
    coil_number = models.TextField(primary_key=True)
    item_obj = models.ForeignKey(ItemMaster,on_delete=models.CASCADE)
    mgo_obj = models.ForeignKey(MGO,on_delete=models.CASCADE)
    pipe_obj = models.ForeignKey(Pipe,on_delete=models.CASCADE)
    conductor_obj = models.ForeignKey(Conductor,on_delete=models.CASCADE)
    mgo_qty = models.DecimalField(max_digits=15, decimal_places=5)
    conductor_qty = models.DecimalField(max_digits=15, decimal_places=5)
    pipe_qty = models.IntegerField()
    coil_diameter = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    
class DrawBenchMaster(models.Model):
    draw_bench_name = models.TextField(primary_key=True)

class FurnaceMaster(models.Model):
    furnace_name = models.TextField(primary_key=True)

class CoilStatus(models.Model):
    coil_number = models.ForeignKey(Coil,on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    coil_diameter  = models.DecimalField(max_digits=15, decimal_places=5,blank=True,null=True)
    status_class = models.CharField(
        max_length=15,
        choices=COIL_STATUS_CLASS,
    )
    draw_bench_name = models.ForeignKey(DrawBenchMaster,on_delete=models.CASCADE,null=True,blank=True)
    furnace_name = models.ForeignKey(FurnaceMaster,on_delete=models.CASCADE, blank=True, null=True)
    
    