from django.contrib import admin
from . models import UserProfile, Contact
from . models import SSC,HSC
from . models import HigherStudies,AfterHsc
from . models import TuitionClass,District,SubDistrict,Subject,Classes
from django.urls import path
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.contrib.admin import ModelAdmin, register



@register(SSC)
class MaterialSSCAdmin(ModelAdmin):
    icon_name = 'person'

class HSCInline(admin.TabularInline):
    model = HSC


class SSCInline(admin.TabularInline):
    model = SSC


class AfterHscInline(admin.TabularInline):
    model = AfterHsc


class HigherStudiesInline(admin.TabularInline):
    model = HigherStudies

class UserProfileAdmin(admin.ModelAdmin):
    inlines = [
        HSCInline,
        SSCInline,
        AfterHscInline,
        HigherStudiesInline,

    ]


class SubDistrictInline(admin.TabularInline):
    model = SubDistrict


class DistrictAdmin(admin.ModelAdmin):
    inlines = [
        SubDistrictInline,
    ]
admin.site.site_header = 'DesireBD Admin Panel'
admin.site.site_title = 'DesireBD Admin Panel'


class UserProfileAdmin(admin.ModelAdmin):
    # fields = ('user', 'blood_group')
    # exclude = ('user', 'blood_group')
    list_display = ('user', 'blood_group', 'genre',
                    'marital_status', 'nationality_html_display', 'profession')
    list_filter = ('blood_group', 'genre', 'marital_status', 'profession')
    change_list_template = 'admin/userprofile/userprofile_change_list.html'
    readonly_fields=('address',)
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
    
    
# Register your models here.
admin.site.register(Contact)
admin.site.register(UserProfile, UserProfileAdmin)
# admin.site.register(SSC)
admin.site.register(HSC)
admin.site.register(AfterHsc)
admin.site.register(HigherStudies)
admin.site.register(TuitionClass)
admin.site.register(District)
admin.site.register(Subject)
admin.site.register(SubDistrict)
admin.site.register(Classes)

