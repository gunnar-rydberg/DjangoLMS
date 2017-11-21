from django.contrib import admin
from .models import Course, Module

# Register your models here.

class ModuleInline(admin.TabularInline):
    model = Module


#admin.site.register(Course)
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_full', 'status')
    list_filter = ('status',)
    inlines = [ModuleInline]

admin.site.register(Module)
