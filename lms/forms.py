from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from .models import Course
import datetime 

class UserCreateForm(forms.ModelForm):
    """ Create new user form """
    is_teacher = forms.BooleanField(label='Teacher user', required=False)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    
    #NOTE that modelfield is more suitable for this really...
    course = forms.TypedChoiceField(label='Course(s)', required=False, empty_value="None", 
        choices=(('','None'),) + tuple(Course.objects.get_choicefield_list()) )

    class Meta:
        model = User
        fields = ('is_teacher', "username", "password1", 'course' )

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

            if self.cleaned_data['is_teacher']:
                group = Group.objects.get(name='Teacher')
                group.user_set.add(user)
            else:
                group = Group.objects.get(name='Student')
                group.user_set.add(user)
            if self.cleaned_data['course'] != '':
                course = Course.objects.get(id = self.cleaned_data['course'] )
                course.students.add(user)
                course.save()
                

        return user





    