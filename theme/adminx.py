#_*_ coding:utf-8 _*_

import xadmin

from theme.models import HomePage

class HomePageAdmin(object):
    list_display = ['title', 'home_title', 'home_title_down', 'nick_name', 'introduction']

xadmin.site.register(HomePage, HomePageAdmin)