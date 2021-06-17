#_*_ coding:utf-8 _*_
from django.urls import path,re_path
from . import views


urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
    re_path(r'article/(?P<article_id>[0-9]+)$',views.ArticleDetailView,name = 'detail'),
    path('archives/',views.ArchiveView.as_view(),name = 'archives'),
    # 分类
    path('categories/',views.CategoryView.as_view(),name = 'categories'),
    # 留言板
    path('commentsboard/',views.MessageForm,name='board'),
    path('tags/',views.TagView.as_view(),name = 'tags'),
    path('tags/<int:tag_id>',views.TagDetailView.as_view(),name = 'tag_detail')
]


