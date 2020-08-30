from django.contrib import admin
from . models import TuitionPost,BlogComment
# Register your models here.


# class TuitionPostAdmin(admin.ModelAdmin):
#     # list_display = ("traduttore", "linguaDa", "linguaA", "prezzoParola",
#     #                 "prezzoRiga", "scontoCat", "scontoFuzzy", "scontoRipetizioni")
#     search_fields = ['subject__Subject_name', 'preferedPlace', 'class_in' ]

admin.site.register(BlogComment)
admin.site.register(TuitionPost)

