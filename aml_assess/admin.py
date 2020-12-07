from django.contrib import admin
from .models import Application, Customer, PEP, Sanction, PotentialMatch

# Register your models here.

admin.site.register(Application)
admin.site.register(Customer)
admin.site.register(PEP)
admin.site.register(Sanction)
admin.site.register(PotentialMatch)

