from email import message
from pyexpat import model
from unicodedata import category
from django.contrib import admin
from .models import Articlemodel, Categorymodel, IPAddress

# Admin header change
admin.site.site_header = 'وبلاگ من'
# Register your models here.
admin.site.disable_action('delete_selected')
def make_published(modeladmin, request, queryset):
    rows_update = queryset.update(status='p')
    if rows_update == 1:
        message_bit = 'منتشر شد'
    else:
        message_bit = 'منتشر شدند' % rows_update
    modeladmin.message_user(request, '{} مقاله {}'.format(rows_update,message_bit))
make_published.short_description = 'انتشار مقالات انتخاب شده'

def make_draft(modeladmin, request, queryset):
    rows_update = queryset.update(status='d')
    if rows_update == 1:
        message_bit = 'پیش نویس شد'
    else:
        message_bit = 'پیش نویس شدند' % rows_update
    modeladmin.message_user(request, '{} مقاله {}'.format(rows_update,message_bit))
make_draft.short_description = ' پیش نویس شدن مقالات '

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug','author','thumbnail','jpublish','is_special','status','category_to_str')
    list_filter = ('publish', 'status','author')
    search_fields = ('title','description')
    prepopulated_fields = {
        'slug':('title',)
    }
    ordering = ['status','publish']
    actions = [make_published, make_draft]
   

def make_published_category(modeladmin, request, queryset):
    rows_update = queryset.update(status=True)
    if rows_update == 1:
        message_bit = 'منتشر شد'
    else:
        message_bit = 'منتشر شدند' % rows_update
    modeladmin.message_user(request, '{} دسته بندی {}'.format(rows_update,message_bit))
make_published_category.short_description = 'انتشار دسته بندی‌های انتخاب شده'

def make_draft_category(modeladmin, request, queryset):
    rows_update = queryset.update(status=False)
    if rows_update == 1:
        message_bit = 'پیش نویس شد'
    else:
        message_bit = 'پیش نویس شدند' % rows_update
    modeladmin.message_user(request, '{} دسته بندی {}'.format(rows_update,message_bit))
make_draft_category.short_description = ' پیش نویس شدن دسته بندی‌ها '


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position','title', 'slug', 'parent', 'status')
    list_filter = ( ['status'])
    search_fields = ('title','slug')
    actions = [make_published_category, make_draft_category]
    prepopulated_fields = {
        'slug':('title',)
    }

admin.site.register(Categorymodel, CategoryAdmin)
admin.site.register(Articlemodel, ArticleAdmin)
admin.site.register(IPAddress)