from django.contrib import admin
# from .models import stadium, snacks, equipment
# Register your models here.
from .models import showcity, showmatch, showsnack

admin.site.register(showcity)
admin.site.register(showmatch)
admin.site.register(showsnack)
# admin.site.register(stadium)
# admin.site.register(snacks)
# admin.site.register(equipment)