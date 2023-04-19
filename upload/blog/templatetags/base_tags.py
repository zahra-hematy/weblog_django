
from datetime import datetime
from django import template
from django.db.models import Count, Q 
from datetime import datetime, timedelta
from ..models import Categorymodel
from ..models import Articlemodel, Categorymodel
from django.contrib.contenttypes.models import ContentType

register = template.Library()

@register.simple_tag
def title():
    return 'وبلاگ جنگویی'


@register.inclusion_tag('blog/partials/category_navbar.html')
def category_navbar():
    return {
         'category':Categorymodel.objects.filter(status='True')
    }

@register.inclusion_tag('blog/partials/sidebar.html')
def popular_articles():
    last_month = datetime.today() - timedelta(days=30)
    return {
         'articles': Articlemodel.objects.published().annotate(
            count=Count('hits', filter=Q(articlehits__created__gt=last_month))
        ).order_by('-count','-publish')[:5],
        "title": "  مقالات پر بازدید ماه"
    }
@register.inclusion_tag('blog/partials/sidebar.html')
def hot_articles():
    last_month = datetime.today() - timedelta(days=30)
    # content_type_id = user_type = ContentType.objects.get(app_label='blog', model='article').id
    return {
         'articles': Articlemodel.objects.published().annotate(
            count=Count('comments', filter=Q(comments__posted__gt=last_month) and Q(comments__content_type_id=6))
        ).order_by('-count','-publish')[:5],
        "title": "  مقالات داغ ماه"
    }

@register.inclusion_tag("registration/partials/link.html")
def link(request, link_name, content, classes):
    return{
        "request": request,
        "link_name": link_name,
        "link": "account:{}".format(link_name),
        "content": content,
        'classes': classes,
    }