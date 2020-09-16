from django.contrib import admin
from .models import Post,PostFile ,ToletComment


class PostFileInline(admin.TabularInline):
    model = PostFile
class PostAdmin(admin.ModelAdmin):
    list_display=('user','category','rent','house_no','road_no','village','post_code','upozila','Zilla')
    search_fields=('user__username','category','rent','house_no','road_no','village','post_code','upozila','Zilla')
    list_filter=('user','category','upozila','Zilla')
    inlines = [
        PostFileInline,
    ]
class ToletCommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user', 'post', 'parent', 'timestamp')
    search_fields = ('comment', 'user__username', 'parent__comment')
    list_filter = ('parent', 'user',)

admin.site.register(Post, PostAdmin)
admin.site.register(ToletComment, ToletCommentAdmin)
