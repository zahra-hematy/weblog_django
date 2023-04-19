from email.policy import default
from multiprocessing.dummy import Manager
from re import A
from tabnanny import verbose
from turtle import update
from django.db import models
from django.utils import timezone
from extensions.utils import jalali_converter
from django.utils.html import format_html
from  account.models import User
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment

# Create your models here.

class ArticleManager (models.Manager):
    def published(self):
        return self.filter(status="p")
class CategoryManager (models.Manager):
    def active(self):
        return self.filter(status=True)
class IPAddress(models.Model):
      ip_address = models.GenericIPAddressField(verbose_name='آدرس آیپی')  
class Categorymodel(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL, related_name='children', verbose_name='عبارت زیر دسته ')
    title = models.CharField(max_length=200, verbose_name = 'عنوان دسته بندی ')
    slug = models.SlugField(max_length=100, unique=True, verbose_name = 'آدرس دسته بندی')
    status = models.BooleanField(default=True, verbose_name='آیا نمایش داده شود؟')
    position = models.IntegerField(verbose_name='پوزیشن')
    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        ordering = ['parent__id','position']
    def __str__(self):
        return self.title
    objects = CategoryManager()
    
class Articlemodel(models.Model):
    STATUS_CHOICES = (
            ('d', 'پیشنویس'),
            ('p', 'منتشر شده'),
            ('i', ' در حال بررسی'),
            ('b', 'برگشت داده شده'),
    )
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='articles', verbose_name='نویسنده' )
    title = models.CharField(max_length=200, verbose_name = 'عنوان مقاله ')
    slug = models.SlugField(max_length=100, unique=True, verbose_name = 'آدرس مقاله')
    category = models.ManyToManyField(Categorymodel, verbose_name='دسته بندی',related_name='articles')
    description = models.TextField(verbose_name = 'محتوا')
    thumbnail = models.ImageField(upload_to='images')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_special = models.BooleanField(default=False, verbose_name='مقاله ویژه ')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name = 'وضعیت')
    comments = GenericRelation(Comment)
    hits = models.ManyToManyField(IPAddress, through='ArticleHits', blank=True, related_name='hits', verbose_name='بازدیدها')

    def get_absoulute_url(self):
        return reverse('account:home')
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ['-publish']

    def jpublish(self):
        return jalali_converter(self.publish)
    jpublish.short_description = 'زمان انتشار'

    # def category_publish(self):
    #     return self.category.filter(status=True)
    def thumbnail_tag(self):
        return format_html("<img width=100 height=75 scr='{}'>".format(self.thumbnail.url))
    thumbnail_tag.short_description ='عکس'

    def category_to_str(self):
        return ",".join([category.title for category in self.category.active()])
    category_to_str.short_description = 'دسته بندی ها'


    objects = ArticleManager()
class ArticleHits(models.Model):
    article = models.ForeignKey(Articlemodel, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)