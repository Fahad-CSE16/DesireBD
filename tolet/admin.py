from django.contrib import admin
from .models import Post,PostFile ,ToletComment, Area, Category


class PostFileInline(admin.TabularInline):
    model = PostFile
class PostAdmin(admin.ModelAdmin):
    list_display=('user','category','rent','district','area')
    search_fields=('user__username','category__name','rent')
    list_filter=('user','category')
    inlines = [
        PostFileInline,
    ]
class ToletCommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user', 'post', 'parent', 'timestamp')
    search_fields = ('comment', 'user__username', 'parent__comment')
    list_filter = ('parent', 'user',)

admin.site.register(Post, PostAdmin)
admin.site.register(ToletComment, ToletCommentAdmin)
admin.site.register(Area)
admin.site.register(Category)
