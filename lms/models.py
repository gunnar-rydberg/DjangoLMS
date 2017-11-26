from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Course(models.Model):
    """ Course """
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

    order = models.IntegerField()

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
        ordering = ['order']

    def __str__(self):
        return self.name

    