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



# See django docs:
# https://docs.djangoproject.com/en/1.11/topics/http/file-uploads/
class UploadFileForm(forms.Form):
    description = forms.CharField(max_length = 200)
    file = forms.FileField()


@permission_required('lms.teacher_rights')
def upload_file(request):
    if request.method == 'POST':
        print("post")
        print(request.FILES)
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            store_uploaded_file(request.FILES['file'])
            return redirect('index')
    else:
        form = UploadFileForm()
    return render(request, r'lms\upload_file.html', {'form':form})


import os

def store_uploaded_file(file):
    file_path = os.path.join('storage', file.name)
    #TODO must create 'storage' folder if not existing
    with open(file_path , 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)


from django.http import HttpResponse

def serve_file(request, file_id):
    print("serving file: {}".format(file_id))
    """ Serve file for download """
    file = open(os.path.join('storage', file_id), 'rb')
    response = HttpResponse(file, content_type ="application/octet-stream")
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_id)
    return response











