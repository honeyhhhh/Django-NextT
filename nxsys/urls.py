"""nxsys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

# #1、导入系统logging
#import logging
# #2、获取日志器
#logger = logging.getLogger('django')
#from django.http import HttpResponse
#
#def log(request):
#    logger.info('info')
#    return HttpResponse('test')

# 网址/admin
import xadmin
xadmin.autodiscover()
from xadmin.plugins import xversion
xversion.register_models()

from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    re_path(r'^xadmin/', xadmin.site.urls),
    #include  元组（urlconf_module子应用路由,app_name子应用名字），namespace防止不同子应用之间相同路由名字冲突
    path('', include(('home.urls','home'), namespace='home')),
    path('', include(('users.urls','users'),namespace='users')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^ueditor/',include('DjangoUeditor.urls')),
    re_path(r'mdeditor/',include('mdeditor.urls')),
 #   path('log/',log),
]



urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
