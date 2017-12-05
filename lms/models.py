from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class PermissionsSupport(models.Model):
    """ Dummy class for setting up general user permissions """
    class Meta:
        managed = False # Don't manage in DB
        permissions = (
            ('teacher_rights', 'Global teacher rights'),
        )


class UserProfile(models.Model):
    """ extends User model """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_course = models.ForeignKey('Course', on_delete=None)


class CourseManager(models.Manager):
    """ Course manager """
    def get_choicefield_list(self):
        return self.values_list('id', 'name').order_by('name')


class Course(models.Model):
    """ Course """
    objects = CourseManager()

    name = models.CharField(max_length=50)
    name_full = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    #TODO documents
    students = models.ManyToManyField(User, help_text="Enrolled stsudents")
    #TODO models.ManyToManyField(User, limit_choices_to=Q(groups__name = 'student'), help_text="Enrolled stsudents")

    #TODO teachers #NOTE is this the same as students because they rely on the same table???

    COURSE_STATUS = (
        ('p', 'Planning'),
        ('r', 'Ready'),
        ('o', 'Open'),
        ('c', 'Closed'), #TODO add status between open and close (waiting for student hand-ins & tests)
    )

    status = models.CharField(max_length=1, choices=COURSE_STATUS, default='p')

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """ Returns detail view """
        return reverse('course-detail', args=[str(self.id)])


class Module(models.Model):
    """ Course module """
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    order = models.IntegerField(null=True)

    course = models.ForeignKey('Course', on_delete=models.CASCADE) #TODO never delete anything!

    #TODO documents

    MODULE_STATUS = (
        ('p', 'Planning'),
        ('r', 'Ready'),
        ('o', 'Open'),
        ('c', 'Closed'),
    )

    status = models.CharField(max_length=1, choices=MODULE_STATUS, default='p')

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """ Returns detail view """
        return reverse('course-detail', args=[str(self.course.id)])


class Activity(models.Model):
    """ Course module """
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    module = models.ForeignKey('Module', on_delete=models.CASCADE) #TODO never delete anything!

    #TODO documents

    ACTIVITY_TYPE = (
        ('l', 'Lecture'),
        ('e', 'E-Learning'),
        ('x', 'Exercise'),
        ('o', 'Other'),
    )

    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPE, default='l')


    def get_activity_type(self):
        return next(name for (key,name) in self.ACTIVITY_TYPE if key == self.activity_type)


    class Meta:
        ordering = ['start_date']


    def __str__(self):
        return self.name

import uuid

class Document(models.Model):
    """ Document handle entity """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    #user = models.ForeignKey(User)
    #date = ...
    course = models.ForeignKey('Course', null=True)

    def get_id(self):
        return str(self.id)

    class Meta:
        ordering = ['file_name']

    



