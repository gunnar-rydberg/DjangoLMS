from django.shortcuts import render
from .models import Course, Module, Document

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
    course_id = forms.CharField(widget = forms.HiddenInput())
    file = forms.FileField()


@permission_required('lms.teacher_rights')
def upload_file(request):
    if request.method == 'POST':
        print("post")
        print(request.FILES)
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            document = Document(file_name = request.FILES['file'].name,
                                description = form.cleaned_data['description'],
                                course = Course.objects.get(pk = form.cleaned_data['course_id']))
            document.save()
            print(document.id)
            store_uploaded_file(request.FILES['file'], document.id, request.FILES['file'].name)
            return redirect('index')
    else:
        form = UploadFileForm(initial = {'course_id': request.GET.get('course_id') } )
    return render(request, r'lms\upload_file.html', {'form':form})


import os

def store_uploaded_file(file, document_id, file_name):
    print("upload method")
    print(document_id)
    path = os.path.join('storage', str(document_id))
    if not os.path.exists(path):
        os.makedirs(path)
    
    with open(os.path.join(path, file_name) , 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)


from django.http import HttpResponse

def serve_file(request, document_id):
    """ Serve file for download """
    document = Document.objects.get(id = document_id)
    print("serving file: {} ({})".format(document.id, document.file_name))
    path = os.path.join('storage',document_id)
    file_name = document.file_name #TODO fetch from db

    file = open(os.path.join(path, file_name), 'rb')
    response = HttpResponse(file, content_type ="application/octet-stream")
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
    return response











