from django.contrib import admin

# Register your models here.
from .models import Comment
from django.urls import reverse
from django.utils.html import format_html



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target', 'nickname', 'content', 'website', 'create_time')



