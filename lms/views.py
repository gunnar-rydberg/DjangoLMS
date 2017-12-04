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
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

class CourseListView(LoginRequiredMixin, generic.ListView):
    model = Course


class CourseDetailView(LoginRequiredMixin, generic.DetailView):
    model = Course

# Teacher rights required
class CourseCreateView(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'lms.teacher_rights'
    model = Course
    fields = ['name','name_full','description','start_date','end_date']
    template_name_suffix = '_create'

from django import forms

class ModuleCreateForm(forms.ModelForm):
    # my_date_field = forms.DateField(
    #     widget=forms.DateInput(format=('%Y-%m-%d'), 
    #                            attrs={'type': 'date',
    #                                'class':'myDateClass', 
    #                            'placeholder':'Select a date'}))

    class Meta:
        model = Module
        fields = ['name','description','start_date','end_date', 'course']
        widgets =  {'course': forms.HiddenInput()}
        

class ModuleCreateView(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'lms.teacher_rights'
    model = Module
    form_class = ModuleCreateForm
    template_name_suffix = '_create'
    

    def get_initial(self):
        return {'course': self.kwargs['course_id']}



from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from .forms import UserCreateForm

@permission_required('lms.teacher_rights')
def create_student(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UserCreateForm()
    return render(request, 'lms\student_create.html', {'form':form})










