from django.db import models
from django.contrib.auth.models import User
import datetime


DAYS_OF_WEEK = (
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
)

class course(models.Model):
    course_name = models.CharField(max_length=30, unique=True)
    course_description = models.CharField(max_length=100)
    course_type = models.CharField(max_length=15)
    course_required_instr_sware = models.CharField(max_length=200, default="MS Office")
    course_required_sware = models.CharField(max_length=200, default="MS Office")
    course_notes = models.CharField(max_length=200, default="MS Office")
    course_last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.course_name

class classroom(models.Model):
    class_name = models.CharField(max_length=30, unique=True)
    class_description = models.CharField(max_length=100)
    class_type = models.CharField(max_length=15)
    class_location = models.CharField(max_length=255)
    class_capacity = models.IntegerField(default=0)
    class_last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.class_name


class schedule(models.Model):
    sch_day = models.CharField(max_length=1, choices=DAYS_OF_WEEK)
    sch_start = models.TimeField(default=datetime.time(00, 00))
    sch_end = models.TimeField(default=datetime.time(00, 00))
    sch_semester = models.IntegerField(default=2020)
    sch_year = models.CharField(max_length=15, default="2019-20")
    #sch_created_at = models.DateTimeField(auto_now_add=True)
    #sch_updated_at = models.DateTimeField(null=True)
    #sch_created_by = models.ForeignKey(User, related_name='schedules', on_delete=models.CASCADE)
    #sch_updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)
    sch_course = models.ForeignKey(course, related_name='course_schedule', on_delete=models.CASCADE) ## One to Many course --> schedules
    sch_instructor = models.ForeignKey(User, related_name='course_ins', on_delete=models.CASCADE) ## One to One instructor --> schedule
    sch_clsroom = models.ForeignKey(classroom, related_name='classrm', on_delete=models.CASCADE) ## One to One Class --> schedule

    def __str__(self):
        return self.sch_instructor

class clas_sware(models.Model):
    sware_name = models.CharField(max_length=30, unique=True)
    sware_description = models.CharField(max_length=100)
    sware_notes = models.CharField(max_length=15)
    sware_last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sware_name


class clas_sware_install(models.Model): ## Many to Many
    sware_id = models.ForeignKey(clas_sware, related_name='classware', on_delete=models.CASCADE) ## One to Many sware --> install 
    classroom_id = models.ForeignKey(classroom, related_name='sware', on_delete=models.CASCADE) ## One to Many  classroom --> sware install 

    def __str__(self):
        return self.sware_id


class clas_hware(models.Model):
    hware_name = models.CharField(max_length=30, unique=True)
    hware_description = models.CharField(max_length=100)
    hware_notes = models.CharField(max_length=15)
    hware_last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.hware_name
		
class clas_hware_deploy(models.Model): ## Many to Many
    hware_id = models.ForeignKey(clas_hware, related_name='clashware', on_delete=models.CASCADE) ## One to Many hware --> deploy 
    classroom_id = models.ForeignKey(classroom, related_name='hware', on_delete=models.CASCADE) ## One to Many  classroom --> hware deploy 

    def __str__(self):
        return self.hware_id
