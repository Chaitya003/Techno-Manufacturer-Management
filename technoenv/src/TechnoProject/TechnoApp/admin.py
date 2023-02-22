from django.contrib import admin
from TechnoApp.models import *

# Register your models here.

admin.site.unregister(User)

# admin.site.register(User)
admin.site.register(TechnoUser)
admin.site.register(ElementMaster)
admin.site.register(AlloyMaster)
admin.site.register(PipeAlloyElementMappingMaster)
admin.site.register(Pipe)
admin.site.register(PipeAlloyElementQuantity)
admin.site.register(ConductorAlloyElementMappingMaster)
admin.site.register(Conductor)
admin.site.register(ConductorAlloyElementQuantity)
admin.site.register(MGOAlloyElementMappingMaster)
admin.site.register(MGO)
admin.site.register(MGOAlloyElementQuantity)
admin.site.register(ItemMaster)
admin.site.register(Coil)
admin.site.register(CoilStatus)
admin.site.register(DrawBenchMaster)
admin.site.register(FurnaceMaster)
# Register your models here.
