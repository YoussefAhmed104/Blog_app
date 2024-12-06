from django.contrib import admin
from .models import * 
# Register your models here
@admin.register(Post)
class PostAdmin (admin.ModelAdmin):
    list_display = ['title', 'auther', 'publish', 'status','slug']
    list_filter = ['status', 'created', 'publish', 'auther']
    search_fields = ['title', 'body']
    raw_id_fields = ['auther']  
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name','body','created']
    list_filter = ['created','updated']
    search_fields = ['name','body']
    