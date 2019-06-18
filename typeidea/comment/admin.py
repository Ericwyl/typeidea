from django.contrib import admin

# Register your models here.
from .models import Comment
from django.urls import reverse
from django.utils.html import format_html
# from typeidea.custom_site import custom_site

from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    site_header = 'Typeidea'
    site_title = 'Typeidea管理后台'
    index_title = '首页'


custom_site = CustomSite(name='cus_admin')



@admin.register(Comment, site=custom_site)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target', 'nickname', 'content', 'website', 'create_time')



