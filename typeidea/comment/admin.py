from django.contrib import admin

# Register your models here.
from .models import Comment
from django.urls import reverse
from django.utils.html import format_html
from typeidea.custom_site import custom_site


@admin.register(Comment, site=custom_site)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target', 'nickname', 'content', 'website', 'create_time')



