from django.contrib import admin
from . models import UserProfile, Contact
from . models import SSC,HSC
from . models import HigherStudies,AfterHsc
from . models import TuitionClass,District,SubDistrict,Subject,Classes


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
# Register your models here.
admin.site.register(Contact)
admin.site.register(UserProfile)
admin.site.register(SSC)
admin.site.register(HSC)
admin.site.register(AfterHsc)
admin.site.register(HigherStudies)
admin.site.register(TuitionClass)
admin.site.register(District)
admin.site.register(Subject)
admin.site.register(SubDistrict)
admin.site.register(Classes)

