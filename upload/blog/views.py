from unicodedata import category
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404,JsonResponse
from .models import Articlemodel, Categorymodel
from django.core.paginator import Paginator
from time import timezone
from account.models import User 
from django.views.generic import ListView, DetailView
from account.mixins import AuthorAccessMixin
from django.db.models import Count, Q 
from datetime import datetime, timedelta
from django.db.models import Q
# Create your views here.
from django.urls import reverse_lazy


class ArticleList(ListView):
    # model = Articlemodel
    # context_object_name = 'articles'
    queryset= Articlemodel.objects.published()
    # template_name = 'blog/home.html'
    paginate_by = 2


class ArticleDetail(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        article =  get_object_or_404(Articlemodel.objects.published(), slug=slug )
        ip_address = self.request.user.ip_address
        if ip_address not in article.hits.all():
            article.hits.add(ip_address)
        return article
class ArticlePreview(AuthorAccessMixin, DetailView):
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Articlemodel, pk=pk )

# def DetailArticleView(request, slug):
#     context = {
        
#         'article': get_object_or_404(Articlemodel.objects.published(), slug=slug ),

#     }

#     return render(request, 'blog/detail.html', context)

# def api(request):
#     data = {
#      '1':{
#         'title': 'first',
#         'id':29,
#         'slug':'firs'
#      },
#         '2': { 
#         'title': 'first',
#         'id':29,
#         'slug':'firs'
#          } }
#     return JsonResponse(data)

# def Category (request, slug, page=1):
#     category = get_object_or_404(Categorymodel, slug=slug, status=True ),

#     articles_list = category.articles.published()
#     paginator = Paginator(articles_list, 3)
#     page = request.GET.get('page')
#     articles = paginator.get_page(page)
#     context = {
        
#         'category': category,
#         'articles': articles
#     }
#     return render(request, 'blog/category.html', context)

class CategoryList(ListView):
    paginate_by = 2
    template_name = 'blog/categorymodel_list.html'
    def get_queryset(self) :
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Categorymodel.objects.active(),slug=slug)
        return category.articles.published()

    def get_context_data(self, **kwrags):
        context = super().get_context_data(**kwrags)
        context['category'] = category
        return context

class AuthorList(ListView):
    paginate_by = 2
    template_name = 'blog/AuthorModel_list.html'
    def get_queryset(self) :
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(Categorymodel.objects.active(),username=username)
        return author.articles.published()

    def get_context_data(self, **kwrags):
        context = super().get_context_data(**kwrags)
        context['author'] = author
        return context
class SearchList(ListView):
    paginate_by = 5
    template_name = 'blog/Search_list.html'
    def get_queryset(self) :
        search = self.request.GET.get('q')
        return Articlemodel.objects.filter(Q(description__icontains=search) | Q(title__icontains=search))

    def get_context_data(self, **kwrags):
        context = super().get_context_data(**kwrags)
        context['search'] = self.request.GET.get('q')
        return context
from django.contrib.auth.views import PasswordResetView
class ForgetPasswordView(PasswordResetView):
     template_name = 'registration/forget_password.html'
     success_url = reverse_lazy('password_reset_done')
     email_template_name = 'registration/reset_password_email.html'
    #  subject_template_name = 'registration/reset_password_subject.txt'
from django.contrib.auth.views import PasswordResetConfirmView


class ResetPasswordConfirmView(PasswordResetConfirmView):
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('login')