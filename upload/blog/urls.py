from unicodedata import name
from django.urls import path



from .views import ArticleDetail,CategoryList, ArticleList,AuthorList, ArticlePreview, SearchList


app_name = 'blog'
urlpatterns = [

    path('',ArticleList.as_view(), name='home'),
    # path('api', api, name='api')
    path('page/<int:page>', ArticleList.as_view(), name='home'),

    path('article/<slug:slug>', ArticleDetail.as_view(), name='detail'),
    path('preview/<int:pk>', ArticlePreview.as_view(), name='preview'),
    path('category/<slug:slug>', CategoryList.as_view(), name='category'),
    path('category/<slug:slug>/<int:page>', CategoryList.as_view(), name='category'),
    path('author/<slug:username>', AuthorList.as_view(), name='author'),
    path('author/<slug:username>/',AuthorList.as_view(), name='author'),
    path('search/', SearchList.as_view(), name='search'),
    path('search/page/<int:page>/',SearchList.as_view(), name='serach'),

]

