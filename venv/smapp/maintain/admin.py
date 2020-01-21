from django.contrib import admin

from .models import course, schedule, classroom, clas_sware

admin.site.register(course)
admin.site.register(schedule)
admin.site.register(classroom)
admin.site.register(clas_sware)
#admin.site.register(clas_sware_install)