Users:

admin
smapp2019




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
    sch_instructor = models.ForeignKey(User, related_name='course_ins', on_delete=models.CASCADE) ## One to Many instructor --> schedule
    sch_clsroom = models.ForeignKey(classroom, related_name='classrm', on_delete=models.CASCADE) ## One to Many Class --> schedule

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


https://stackoverflow.com/questions/3414247/how-to-drop-all-tables-from-the-database-with-manage-py-cli-in-django
https://www.gungorbudak.com/blog/2015/04/13/how-to-clear-or-drop-db-table-of-a-django-app/
python manage.py migrate maintain zero


If you are working in django 1.9.5 this is the 100 % solution for this problem:

1. Delete your migrations folder

2. In the database: DELETE FROM django_migrations WHERE app = 'app_name'.
   You could alternatively just truncate this table.

3. python manage.py makemigrations app_name

4. python manage.py migrate

CREATE TABLE "maintain_schedule" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "sch_day" varchar(3) NOT NULL, "sch_start" time NOT NULL, "sch_end" time NOT NULL, "sch_semester" varchar(40) NOT NULL, "sch_year" varchar(15) NOT NULL, "sch_course_id" integer NOT NULL REFERENCES "maintain_course" ("id") DEFERRABLE INITIALLY DEFERRED)



CREATE TABLE "maintain_clas_sware_install" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
 "sware_id" integer NOT NULL REFERENCES "maintain_clas_sware" ("id") DEFERRABLE INITIALLY DEFERRED,
 "classroom_id" integer NOT NULL REFERENCES "maintain_classroom" ("id") DEFERRABLE INITIALLY DEFERRED)
 
 
 CREATE TABLE "maintain_clas_hware_deploy" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
 "hware_id_id" integer NOT NULL REFERENCES "maintain_clas_hware" ("id") DEFERRABLE INITIALLY DEFERRED,
 "classroom_id_id" integer NOT NULL REFERENCES "maintain_classroom" ("id") DEFERRABLE INITIALLY DEFERRED)

--Init Data

INSERT INTO maintain_classroom (class_name, class_description, class_type, class_location, class_capacity, class_last_updated)
VALUES
    ("OSS333", "OSS333", "Lecture", "O'Shaughnessy Science Hall (OSS)", 30,datetime('now','localtime')),
    ("OSS327", "OSS327", "Lecture", "O'Shaughnessy Science Hall (OSS)", 28,datetime('now','localtime')),
	("OSS325", "OSS325", "Lecture", "O'Shaughnessy Science Hall (OSS)", 35,datetime('now','localtime')),
    ("OSS313", "OSS313", "Lab", "O'Shaughnessy Science Hall (OSS)", 32,datetime('now','localtime')); 

INSERT INTO maintain_course (course_name, course_description, course_type, course_notes, course_last_updated, course_clsroom_id)
VALUES
    ("Software Engineering", "Software Engineering", "Lecture", "Required MS Office by default", datetime('now','localtime'),  1),
    ("Data Mining & Machine Learning", "Data Science", "Lecture", "Required Python for all", datetime('now','localtime'), 2),
	("Introductory Statistics II", "Mathematics", "Lecture", "Required SAS Studio", datetime('now','localtime'), 3),
    ("Statistics I (Lab)", "Mathematics", "Lab", "Required SAS Studio", datetime('now','localtime'), 4); 
	
#ManyToMany
INSERT INTO maintain_course_course_instructor (course_id, user_id)
VALUES
    (1, 1),
    (2, 4),
	(3, 5),
    (3, 6); 


INSERT INTO maintain_schedule (sch_day, sch_start, sch_end, sch_semester, sch_year, sch_course_id)
VALUES
    ('MON', '17:45:00', '21:00:00', "Spring 2020", "2019-20", 1),
    ('WED', '13:35:00', '15:10:00', "Spring 2020", "2019-20", 2),
	('FRI', '08:00:00', '09:40:00', "Spring 2020", "2019-20", 3),
    ('TUE', '09:55:00', '11:35:00', "Spring 2020", "2019-20", 4); 
	

INSERT INTO maintain_clas_sware (sware_name, sware_description, sware_notes, sware_last_updated)
VALUES
    ("Python", "Python Programming Tool", "Additional Libraries - ANaconda",datetime('now','localtime')),
    ("Matlab", "Mathematicians box", "Version must be",datetime('now','localtime')),
	("MathWorks", "Maths and Stuff", "Latest release",datetime('now','localtime')),
    ("SAS Studio", "Statistician and Maths", "Desktop shortcut needed",datetime('now','localtime')); 
	

#ManyToMany
INSERT INTO maintain_clas_sware_sware_classroom (clas_sware_id, classroom_id)
VALUES
    (1, 2),
    (2, 3),
	(3, 3),
    (4, 4); 
	
### Hardware Pending