from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from home.models import Article, Category, MessageBoard, Comment, Tag
from theme.models import HomePage

from django.urls import reverse
from django.shortcuts import  redirect
import logging
logger=logging.getLogger('django')

import markdown
import re



class IndexView(generic.ListView):
    '''
    主页
    '''
    template_name = 'blog/index.html'
    paginate_by = 5
    object = Article

    def get(self, request, *args, **kwargs):
        lists = Article.objects.all()
        #mess = HomePage.objects.all()
        all_categories = Category.objects.all().order_by('index')
        try:
            page = request.GET.get('page', 1)
        except:
            page = 1
        p = Paginator(lists, 5, request=request)
        articles = p.page(page)
        return render(request, "blog/index.html", {
            "lists": articles,
			"all_categories": all_categories
        })

class ArchiveView(generic.ListView):
    '''
    归档
    '''
    template_name = 'blog/archives.html'

    def get(self, request, *args, **kwargs):
        all_articles = Article.objects.all()
        return render(request, "blog/archives.html", {
            "all_articles": all_articles
        })


def ArticleDetailView(request, article_id):
    '''
    文章内容
    '''
    if request.method == "GET":
        post = get_object_or_404(Article, id=article_id)

        # +
        comments=Comment.objects.filter(article=post).order_by('-created_time')


        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return render(request, 'blog/detail.html', context={'post': post, 'comments': comments})


    if request.method == "POST":
        article_id=request.POST.get('id')
        post = get_object_or_404(Article, id=article_id)
        comment = Comment()
        text = request.POST.get("text", "")
        comment.article = post
        comment.content = text
        comment.save()
        #path=reverse('home:detail',args=(article_id))+'#comment_dot'
        return redirect(request.META['HTTP_REFERER'])#HttpResponseRedirect(path)








class CategoryView(generic.ListView):
    """
    文章分类
    """

    def get(self, request, *args, **kwargs):
        all_categories = Category.objects.all().order_by('index')
        return render(request, 'blog/categories.html', locals())


class TagView(generic.ListView):
    def get(self, request):
        all_tag = Tag.objects.all()
        tag_nums = Tag.objects.values().count()
        return render(request, 'blog/tags.html', {'all_tag': all_tag, 'tag_nums':tag_nums})

class TagDetailView(generic.ListView):
    def get(self, request, tag_id):
        tag = get_object_or_404(Tag, id=tag_id)
        tag_article = tag.article_set.all()
        return render(request,'blog/tag_detail.html',{'tag_name':tag.tagname, 'tag_article':tag_article})



def MessageForm(request):

    if request.method == "POST":
        comment = MessageBoard()
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        url = request.POST.get("url", "")
        text = request.POST.get("text", "")
        comment.name = name
        comment.email = email
        comment.url = url
        comment.text = text
        comment.save()
        return HttpResponseRedirect('/commentsboard/')

    if request.method == "GET":
        all_messages = MessageBoard.objects.all().order_by('-created_time')
        try:
            page = request.GET.get('page', 1)
        except:
            page = 1
        p = Paginator(all_messages, 10, request=request)
        comments = p.page(page)
        return render(request, "blog/commentsboard.html", {
            "all_messages": comments,
            "Total":all_messages
        })
