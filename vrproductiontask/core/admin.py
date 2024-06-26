from re import search
from django.contrib import admin

from core.models import Blog, BlogCategory, BlogComment,Tag,About,WebsiteSetting,SocialAccount

admin.site.register(SocialAccount)
admin.site.register(WebsiteSetting)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    readonly_fields = ['author','slug']
    list_display = ('title',  'created_at',)
    list_filter = ( 'created_at', )
    search_fields = ('title', )

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent_cat', )
    search_fields = ('title','parent_cat',)

@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    readonly_fields = ['user',]
    list_filter = ( 'user','created_at', )
    search_fields = ('blog',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', )
    search_fields = ('title', 'created_at', )
    list_filter = ('created_at', )
