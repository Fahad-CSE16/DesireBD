from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.contrib.admin import ModelAdmin, register
from .models import (Country, Education, Expectaion, Address, Body, Family, Height, Hobby, Language, Occupation, Personal_Info, Profession, Religion, Sir_name, State,Weight
)
class ExpectaionAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'marital_status', 'min_age', 'max_age', 'min_height', 'max_height', 'education', 'profession','religion', 'residency_country')
    search_fields = ('user__username', 'marital_status', 'min_age', 'max_age', 'min_height', 'max_height', 'education', 'profession','religion', 'residency_country')
    list_filter = ('min_height', 'max_height', 'min_age', 'max_age', 'religion', 'residency_country', 'education', 'profession',)
class AddressAdmin(ModelAdmin):
    list_display = ('id', 'user','district','state','residency_country','birth_country','grow_up_country','present_address','permanent_address')
    search_fields = ('user__username','district','state','residency_country','birth_country','grow_up_country','present_address','permanent_address')
    list_filter=('district','state','residency_country','birth_country','grow_up_country','present_address','permanent_address')
class BodyAdmin(ModelAdmin):
    list_display = ('id', 'user','height','weight','eye_color','hair_color','hair_style','complexion','body_type','any_disability')
    search_fields = ('user__username','height','weight','eye_color','hair_color','hair_style','complexion','body_type','any_disability')
    list_filter=('height','weight','eye_color','hair_color','hair_style','complexion','body_type','any_disability')
class Personal_infoAdmin(ModelAdmin):
    list_display = ('id', 'user','gender','blood_group','full_name','sir_name','marital_status','phone','is_phone_public','age','birth_date','religion','highest_degree_of_education','mother_tongue')
    search_fields = ('user__username', 'gender', 'blood_group', 'full_name', 'sir_name', 'marital_status', 'phone',
                     'is_phone_public', 'age', 'birth_date', 'religion', 'highest_degree_of_education', 'mother_tongue')
    list_filter = ('gender', 'blood_group', 'full_name', 'sir_name', 'marital_status', 'phone',
                   'is_phone_public', 'age', 'birth_date', 'religion', 'highest_degree_of_education', 'mother_tongue')
class HobbyAdmin(ModelAdmin):
    list_display = ('id', 'user','hobbies','interest','music','read_books','tv_shows','sports_shows','sports','fav_dress_style','fav_color')
    search_fields = ('user__username', 'hobbies', 'interest', 'music', 'read_books',
                     'tv_shows', 'sports_shows', 'sports', 'fav_dress_style', 'fav_color')
    list_filter=('hobbies','interest','music','read_books','tv_shows','sports_shows','sports','fav_dress_style','fav_color')
class FamilyAdmin(ModelAdmin):
    list_display = ('id', 'user','father_name','fathers_occupation','mother_name','mothers_occupation','family_type','family_status','no_of_bro_sis')
    search_fields = ('user__username','father_name','fathers_occupation','mother_name','mothers_occupation','family_type','family_status','no_of_bro_sis')
    list_filter=('father_name','fathers_occupation','mother_name','mothers_occupation','family_type','family_status','no_of_bro_sis')
class OccupationAdmin(ModelAdmin):
    list_display = ('id', 'user','occupation','work_location','salary','employed_by','company','work_from')
    search_fields = ('user__username','occupation','work_location','salary','employed_by','company','work_from')
    list_filter=('occupation','work_location','salary','employed_by','company','work_from')
# Register your models here.
admin.site.register(Expectaion,ExpectaionAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(Hobby, HobbyAdmin)
admin.site.register(Body,BodyAdmin)
admin.site.register(Personal_Info,Personal_infoAdmin)
admin.site.register(Occupation,OccupationAdmin)
admin.site.register(Family,FamilyAdmin)
admin.site.register(Language)
admin.site.register(Height)
admin.site.register(Profession)
admin.site.register(Education)
admin.site.register(Religion)
admin.site.register(Country)
admin.site.register(Sir_name)
admin.site.register(Weight)
admin.site.register(State)
