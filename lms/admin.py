from django.contrib import admin
from .models import Course, Module, Activity, Document

class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 0


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0
    inlines = [ActivityInline]


#admin.site.register(Course)
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_full', 'status')
    list_filter = ('status',)
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_filter = ('course','status')
    inlines = [ActivityInline]


admin.site.register(Activity)
admin.site.register(Document)
