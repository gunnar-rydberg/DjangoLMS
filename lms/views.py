from django.shortcuts import render
from .models import Course, Module

# Create your views here.

#from django.contrib.auth.decorators import login_required
#@login_required
def index(request):
    """ home page of site """

    return render(
        request,
        'index.html')


from django.views import generic
from django.contrib.auth.decorators import  permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

class CourseListView(generic.ListView):
    model = Course


class CourseDetailView(generic.DetailView):
    model = Course

# Teacher rights required
class CourseCreateView(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'lms.teacher_rights'
    model = Course
    fields = ['name','name_full','description','start_date','end_date']
    template_name_suffix = '_create'
