from django.contrib import admin

from .models import course, classroom, clas_sware, clas_hware

<<<<<<< HEAD

=======
admin.site.site_url = "/maintain/"
>>>>>>> 7f4a9991ac37a8284e1c69b428d63580d82388b5

class HwareInline(admin.TabularInline):
    model = clas_hware.hware_classroom.through

class CourseInstructorInline(admin.TabularInline):
    model = course.course_instructor.through

class CourseClassroomInline(admin.TabularInline):
    model = course.course_clsroom.through


@admin.register(course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'course_code', 'course_notes', 'course_meeting_location', 'primary_instr_name',)
    list_per_page = 15
    list_editable = ( 'course_notes', )
    search_fields = ('course_name', 'course_code', 'course_meeting_location', )
    inlines = [
        CourseInstructorInline,
    ]
    exclude = ('course_instructor', 'course_clsroom',)
#admin.site.register(course)
#admin.site.register(schedule)


@admin.register(classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'class_location', 'class_capacity', 'class_computers', 'class_instr_computer')
    list_per_page = 15
    list_editable = ( 'class_capacity', 'class_computers', 'class_instr_computer', )
    search_fields = ('class_name', 'class_location', 'class_capacity')
    inlines = [
        HwareInline,
    ]

@admin.register(clas_sware)
class ClassSwareAdmin(admin.ModelAdmin):
    list_display = ('sware_name', 'sware_version', 'sware_description', 'sware_notes')
    search_fields = ('sware_name', 'sware_version', 'sware_description')
    list_editable = ( 'sware_version', 'sware_description', 'sware_notes', )
    list_per_page = 15


'''@admin.register(clas_hware)
class ClasshwareAdmin(admin.ModelAdmin):
    list_display = ('hware_name', 'hware_description')
    search_fields = ('hware_name', 'hware_description')
    inlines = [
        HwareInline,
    ]
    exclude = ('hware_classroom',)'''


#admin.site.register(classroom)
#admin.site.register(clas_sware)
#admin.site.register(clas_sware_install)