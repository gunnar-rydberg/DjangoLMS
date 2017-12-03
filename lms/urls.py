from django.conf.urls import url
from . import views

urlpatterns = [
#    url(r'^index/', some_view_function),
    url(r'^index/$', views.index, name='index'),
    url(r'^$', views.index, name='index'),
    url(r'^courses/$', views.CourseListView.as_view(), name='courses'),
    url(r'course/(?P<pk>\d+)$', views.CourseDetailView.as_view(), name='course-detail'), 
    url(r'course-create/$', views.CourseCreateView.as_view(), name='course-create'),
    url(r'student-create/$', views.create_student, name='student-create'),

]
