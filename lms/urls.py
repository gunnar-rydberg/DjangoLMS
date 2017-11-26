from django.conf.urls import url
from . import views

urlpatterns = [
#    url(r'^index/', some_view_function),
    url(r'^/index/$', views.index, name='index'),
    url(r'^$', views.index, name='index'),
    url(r'^courses/$', views.CourseListView.as_view(), name='courses'),
    url(r'course/(?P<pk>\d+)$', views.CourseDetailView.as_view(), name='course-detail'), # pk is expected by generic views

]
