# -*- coding: utf-8 -*-
from custom_site import custom_site

from base_admin import BaseOwnerAdmin

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .adminforms import PostAdminForm

# Register your models here.
from .models import Post, Category, Tag
from django.contrib.admin import AdminSite
from django.contrib.admin.models import LogEntry

from django.contrib.admin import AdminSite
# from xadmin.layout import Row, Fieldset
#
# from xadmin.filters import manager
# from xadmin.filters import RelatedFieldListFilter


class PostInline(admin.TabularInline):
    fields = ('title', 'desc')
    extra = 1
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    # inlines = [PostInline]
    '''display页面显示的字段'''
    list_display = ('name', 'status', 'is_nav', 'create_time', 'post_count')
    '''
    fields作用是控制页面上要展示的字段
    '''
    fields = ('name', 'status', 'is_nav')
    '''
    obj 是当前要保存的对像，通过给obj.owner赋值，就能达到自动设置owner的目的，
    request  是当前请求，request.user就是当前已经登陆的用户，如果用户未登陆，拿到的时匿名用户
    form是页面提交过来的表单之后的对象
    change是用户标志本次提交的数据是新增的还是更新的
    '''
    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = '文章数量'

    def __str__(self):
        return self.name


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'create_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(admin.SimpleListFilter):
    '''自定义过滤器只展示当前用户分类'''
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = [
        'title', 'category', 'status', 'create_time', 'operator', 'owner'
    ]
    list_display_links = []

    list_filter = [CategoryOwnerFilter, ]
    search_fields = ['title', 'category__name']

    actions_on_top = True
    # actions_on_bottom = True

    # 编辑页面
    save_on_top = True
    exclude = ['owner']

    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )

    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            )

        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),

        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': ('tag',),

        })
    )
    # filter_horizontal = ('tag',)
    filter_vertical = ('tag',)

    #展示自定义字段
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            # reverse('admin:blog_post_change', args=(obj.id,))
            reverse('cus_admin:blog_post_change', args=(obj.id,))

        )

    operator.short_description = '操作'

    '''
    增加js代码，完成前端操作
    '''
    class Meta:
        css = {
            'all': ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css',),

        }
        js = ('https://cdn.bootcss.com/bootstrap/4.0.0-brta.2/js/bootstrap.bundle.js',)


    #
    # def post_count(self, obj):
    #     return obj.post_set.count()
    #
    # post_count.short_description = 'postadmin'


@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']
