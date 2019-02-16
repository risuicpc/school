from django.contrib import admin

from .models import *

admin.site.register(Grade)
admin.site.register(Subject)
admin.site.register(Room)
admin.site.register(StudentRoom)
admin.site.register(Teach)