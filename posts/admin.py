from django.contrib import admin
from . models import TuitionPost,BlogComment
from django.contrib.admin import ModelAdmin
from django.utils import timezone
# Register your models here.


class TuitionPostAdmin(admin.ModelAdmin):
    list_display = ('author', 'district', 'created_since','get_subjects','salary')
    list_filter = ('author', 'district', 'subject', 'class_in')
    actions = ('set_district_gazipur',)
    search_fields = ('content', 'author__username', 'subject__name', 'district__name', 'class_in__name')
    # list_select_related=('district',)
    list_display_links = ('author', 'district',)
    list_editable = ('salary',)
    filter_vertical= ('subject','class_in','preferedPlace','views','likes')
    def created_since(self, TuitionPost):
        diff = timezone.now() - TuitionPost.timeStamp
        return diff.days
    created_since.short_description = ' Since Created'
    def set_district_gazipur(self, request, queryset):
        count = queryset.update(district=1)
        self.message_user(request, '{} posts updated'.format(count))
    set_district_gazipur.short_description='Set District to Gazipur'
    def get_subjects(self, obj):
        return ", ".join([p.name for p in obj.subject.all()])
    get_subjects.short_description = 'Subjects'
    

admin.site.register(BlogComment)
admin.site.register(TuitionPost, TuitionPostAdmin)

