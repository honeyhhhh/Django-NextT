#_*_ coding:utf-8 _*_
import xadmin

from xadmin.plugins.multiselect import *  

from home.models import Article,Tag ,Category, MessageBoard,Comment




class ArticleAdmin(object):
    list_display = ['title', 'category', 'art_tags','created_time', 'modified_time','views']
    search_fields = ['title','tags']
    list_filter = ['category', 'created_time', 'tags','modified_time']
    list_editable = ['title', 'categoty']
    filter_horizontal= ('Tag',)
    style_fields = {'tags':'checkbox-inline'}
    
xadmin.site.register(Article, ArticleAdmin)

class TagAdmin(object):
    search_fields = ['tagname']
    list_filter = ['tagname']

xadmin.site.register(Tag, TagAdmin)

class CategoryAdmin(object):
    list_display = ['name', 'index']
    search_fields = ['name', 'index']
    list_filter = ['name', 'index']
    list_editable = ['name', 'index']

xadmin.site.register(Category, CategoryAdmin)

class MessageBoardAdmin(object):
    list_display = ['name', 'email', 'url', 'created_time']

xadmin.site.register(MessageBoard, MessageBoardAdmin)

class CommentAdmin(object):
    list_display = ['content','article','created_time']

xadmin.site.register(Comment, CommentAdmin)
