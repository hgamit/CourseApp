from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils.text import Truncator
from django.utils.html import mark_safe
from markdown import markdown

class classroom(models.Model):
    class_name = models.CharField(max_length=30, unique=True)
    #class_description = models.CharField(max_length=100)
    #class_type = models.CharField(max_length=15)
    class_location = models.CharField(max_length=255)
    class_capacity = models.IntegerField(default=0)
    class_computers = models.IntegerField(default=0)
    class_instr_computer = models.BooleanField(default=False)
    class_last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.class_name

class course(models.Model):
    course_name = models.CharField(max_length=30, default="Unknown")
    course_code = models.CharField(max_length=10, default="Unknown")
    course_section = models.CharField(max_length=10, default="Unknown")
    course_site = models.CharField(max_length=10, default='Unknown')
    course_meeting_location = models.CharField(max_length=10, default="Unknown")
    course_description = models.CharField(max_length=300, default='No Description yet.')
    course_type = models.CharField(max_length=15, default="Unknown")
    course_level = models.CharField(max_length=15, default="Unknown")
    #course_required_instr_sware = models.CharField(max_length=200, default="MS Office")
    #course_required_sware = models.CharField(max_length=200, default="MS Office")
    course_notes = models.CharField(max_length=200, default="Unknown")
    course_last_updated = models.DateTimeField(auto_now_add=True)
    course_instructor = models.ManyToManyField(User, related_name='course_ins') ## Many to Many instructor --> course
    course_clsroom = models.ManyToManyField(classroom, related_name='classrm') ## Many to Many Class --> course
    sch_days = models.CharField(max_length=8, default='Unknown')
    sch_timeslot= models.CharField(max_length=10, default='Unknown')
    sch_dateslot= models.CharField(max_length=70, default='Unknown')
    sch_semester = models.CharField(max_length=40,default="Unknown")
    sch_year = models.CharField(max_length=15, default="Unknown")
    primary_instr_name = models.CharField(max_length=40,default="Unknown")
    updatedby_name = models.CharField(max_length=40,default="Unknown")

    def __str__(self):
        return self.course_name

    def get_posts_count(self):
        return post.objects.filter(post_topic__topic_course=self).count()

    def get_last_post(self):
        return post.objects.filter(post_topic__topic_course=self).order_by('-post_created_at').first()

'''class schedule(models.Model):
    MONDAY = "MON"
    TUESDAY = "TUE"
    WEDNESDAY = "WED"
    THURSDAY = "THU"
    FRIDAY = "FRI"
    SATURDAY = "SAT"
    SUNDAY = "SUN"
    DAYS_OF_WEEK = (
    (MONDAY, 'Monday'),
    (TUESDAY, 'Tuesday'),
    (WEDNESDAY, 'Wednesday'),
    (THURSDAY, 'Thursday'),
    (FRIDAY, 'Friday'),
    (SATURDAY, 'Saturday'),
    (SUNDAY, 'Sunday'), )

    sch_days = models.CharField(max_length=8, default='M')
    sch_timeslot= models.CharField(max_length=10, default='1745-2100')
    sch_dateslot= models.CharField(max_length=12, default='2/4-5/20')
    #sch_start = models.TimeField(default=datetime.time(00, 00))
    #sch_end = models.TimeField(default=datetime.time(00, 00))
    sch_semester = models.CharField(max_length=40,default="Spring 2020")
    sch_year = models.CharField(max_length=15, default="2019-20")
    #sch_created_at = models.DateTimeField(auto_now_add=True)
    #sch_updated_at = models.DateTimeField(null=True)
    #sch_created_by = models.ForeignKey(User, related_name='schedules', on_delete=models.CASCADE)
    #sch_updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)
    sch_course = models.OneToOneField(course, related_name='course_schedule', on_delete=models.CASCADE) ## One to Many course --> schedules
    
    def __str__(self):
        return self.sch_semester'''

class clas_sware(models.Model):
    sware_name = models.CharField(max_length=30, unique=True)
    sware_version = models.CharField(max_length=40, default= None)
    sware_description = models.CharField(max_length=250,default='No Description yet.')
    sware_notes = models.CharField(max_length=200, default='No Notes yet.')
    sware_last_updated = models.DateTimeField(auto_now_add=True)
    sware_classroom = models.ManyToManyField(classroom, related_name='sware') ## Many to Many  classroom --> sware  

    def __str__(self):
        return self.sware_name


class clas_hware(models.Model):
    hware_name = models.CharField(max_length=30, unique=True)
    hware_description = models.CharField(max_length=100, default='No Description yet.')
    #hware_notes = models.CharField(max_length=15)
    hware_last_updated = models.DateTimeField(auto_now_add=True)
    hware_classroom = models.ManyToManyField(classroom, related_name='hware') ## Many to Many  classroom --> sware  

    def __str__(self):
        return self.hware_name
		

'''class clas_sware_install(models.Model): ## Many to Many
    sware = models.ForeignKey(clas_sware, related_name='classware1', on_delete=models.CASCADE) ## One to Many sware --> install 
    classroom = models.ForeignKey(classroom, related_name='sware1', on_delete=models.CASCADE) ## One to Many  classroom --> sware install 

    def __str__(self):
        return self.sware

class clas_hware_deploy(models.Model): ## Many to Many
    hware_id = models.ForeignKey(clas_hware, related_name='clashware1', on_delete=models.CASCADE) ## One to Many hware --> deploy 
    classroom_id = models.ForeignKey(classroom, related_name='hware1', on_delete=models.CASCADE) ## One to Many  classroom --> hware deploy 

    def __str__(self):
        return self.hware_id'''


class topic(models.Model):
    topic_subject = models.CharField(max_length=255)
    topic_software = models.CharField(max_length=255, default=None)
    topic_last_updated = models.DateTimeField(auto_now_add=True)
    topic_course = models.ForeignKey(course, related_name='course_topics', on_delete=models.CASCADE)
    topic_starter = models.ForeignKey(User, related_name='user_topics', on_delete=models.CASCADE)
    topic_views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.topic_subject

class post(models.Model):
    post_message = models.TextField(max_length=4000)
    post_topic = models.ForeignKey(topic, related_name='topic_posts', on_delete=models.CASCADE)
    post_created_at = models.DateTimeField(auto_now_add=True)
    post_updated_at = models.DateTimeField(null=True)
    post_created_by = models.ForeignKey(User, related_name='user_posts', on_delete=models.CASCADE)
    post_updated_by = models.ForeignKey(User, blank=True, null=True, related_name='+', on_delete=models.CASCADE)


    def __str__(self):
        truncated_message = Truncator(self.post_message)
        return truncated_message.chars(30)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.post_message, safe_mode='escape'))


class userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    notification = models.BooleanField(default=False)
