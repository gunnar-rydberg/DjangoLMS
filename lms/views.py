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

class CourseListView(generic.ListView):
    model = Course


class CourseDetailView(generic.DetailView):
    model = Course


    