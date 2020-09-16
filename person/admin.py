from django.contrib import admin
from . models import UserProfile, Contact
from . models import SSC,HSC
from . models import HigherStudies,AfterHsc
from . models import TuitionClass,District,SubDistrict,Subject,Classes
from django.urls import path
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.contrib.admin import ModelAdmin, register
admin.site.site_header = 'DesireBD Admin Panel'
admin.site.site_title = 'DesireBD Admin Panel'
admin.site.index_title = ''



class SubDistrictInline(admin.TabularInline):
    model = SubDistrict

class DistrictAdmin(admin.ModelAdmin):
    inlines = [
        SubDistrictInline,
    ]
class UserProfileAdmin(admin.ModelAdmin):
    # fields = ('user', 'blood_group')
    # exclude = ('user', 'blood_group')
    # readonly_fields = ('address',)
    list_display = ('user', 'blood_group', 'genre',
                    'marital_status', 'nationality_html_display', 'profession')
    list_filter = ('blood_group', 'genre', 'marital_status', 'profession')
    search_fields=('user__username','blood_group','profession','address')
    change_list_template = 'admin/userprofile/userprofile_change_list.html'
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('fontsize/<str:slug>/', self.change_nationality)
        ]
        return custom_urls+ urls
    def change_nationality(self, request, slug):
        self.model.objects.all().update(nationality=slug)
        return HttpResponseRedirect("/admin/person/userprofile/")
    def nationality_html_display(self, obj):
        return format_html(
            f'<span style="font-size: 20px; color:blue;"> {obj.nationality}</span> '
        )


class AfterHscAdmin(admin.ModelAdmin):
    list_display = ('user', 'Etype', 'degree', 'institute','cgpa','passing_year')
    list_filter = ('Etype', 'degree', 'institute', 'cgpa', 'passing_year')
    search_fields=('user__username','Etype', 'degree', 'institute', 'cgpa', 'passing_year')
class SSCAdmin(admin.ModelAdmin):
    list_display=('user','group','board','institute','gpa','passing_year',)
    search_fields=('user__username','group','board','institute','gpa','passing_year',)
    list_filter=('group','board','institute','gpa','passing_year',)
class HSCAdmin(admin.ModelAdmin):
    list_display=('user','group','board','institute','gpa','passing_year',)
    search_fields=('user__username','group','board','institute','gpa','passing_year',)
    list_filter = ('group', 'board', 'institute', 'gpa', 'passing_year',)
class HigherStudiesAdmin(admin.ModelAdmin):
    list_display=('user','masters','phd')
    search_fields = ('user__username', 'masters', 'phd')
    list_filter = ('user', 'masters', 'phd')
class ContactAdmin(admin.ModelAdmin):
    list_display = ('sno', 'name', 'email', 'phone', 'timeStamp')
    search_fields = ('sno', 'name', 'email', 'phone', 'timeStamp')
    list_filter = ( 'name', 'email', 'phone',)
class TuitionClassAdmin(admin.ModelAdmin):
    list_display = ('user', 'district', 'style',
                     'approach', 'get_subjects', 'get_level','medium','salary','days','status')
    list_filter = ('district', 'subject', 'level', 'status')
    search_fields = ( 'user__username',
                     'subject__name', 'district__name', 'level__name')
    list_display_links = ('user', 'district',)
    filter_horizontal = ('subject', 'level',
                       'preferedPlace')
    def get_subjects(self, obj):
        return ", ".join([p.name for p in obj.subject.all()])
    get_subjects.short_description = 'Subjects'
    def get_level(self, obj):
        return ", ".join([p.name for p in obj.level.all()])
    get_level.short_description = 'level'
# Register your models here.
admin.site.register(SSC, SSCAdmin)
# admin.site.register(SubDistrict)
admin.site.register(Contact, ContactAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(HSC, HSCAdmin)
admin.site.register(AfterHsc, AfterHscAdmin)
admin.site.register(HigherStudies, HigherStudiesAdmin)
admin.site.register(TuitionClass, TuitionClassAdmin)
admin.site.register(District,DistrictAdmin)
admin.site.register(Subject)
admin.site.register(Classes)

