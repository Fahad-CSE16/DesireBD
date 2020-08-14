from django.contrib import admin
from .models import Post,PostFile ,ToletComment


class PostFileInline(admin.TabularInline):
    model = PostFile


class PostAdmin(admin.ModelAdmin):
    inlines = [
        PostFileInline,
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(ToletComment)
