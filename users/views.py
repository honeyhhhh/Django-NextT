from django.shortcuts import render
from django.views import View
from django.http.response import HttpResponseBadRequest
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from django.http import HttpResponse
from django.shortcuts import  redirect
from django.urls import reverse
import json

from django.http import JsonResponse
from random import randint
from libs.aliyun.sms import send_sms
import logging
logger=logging.getLogger('django')
from utils.response_code import RETCODE
import requests
import base64
import rsa
from bs4 import BeautifulSoup as bs
import urllib



# Create your views here.

def check(std_no,password):
    yhm=str(std_no)
    url='http://www.zfjw.xupt.edu.cn/jwglxt/xtgl/login_slogin.html'
    mm=bytes(password,encoding="utf8")
    session = requests.Session()
    publickey = session.get('http://www.zfjw.xupt.edu.cn/jwglxt/xtgl/login_getPublicKey.html').json()
    b_modulus=base64.b64decode(publickey['modulus'])#将base64解码转为bytes
    b_exponent=base64.b64decode(publickey['exponent'])#将base64解码转为bytes
    #公钥生成,python3从bytes中获取int:int.from_bytes(bstring,'big')
    mm_key = rsa.PublicKey(int.from_bytes(b_modulus,'big'),int.from_bytes(b_exponent,'big'))
    #利用公钥加密,bytes转为base64编码
    rsa_mm = base64.b64encode(rsa.encrypt(mm, mm_key))
    page = session.get(url)
    soup = bs(page.text,"html.parser")
    #获取认证口令csrftoken
    csrftoken = soup.find(id="csrftoken").get("value")
    postdata={'csrftoken':csrftoken,'language': 'zh_CN','yhm':yhm,'mm':rsa_mm,'mm':rsa_mm}
    # print(postdata)
    #f = open('test.html','wb')
    rq=session.post(url,data=postdata)
    # f.write(rq.content)
    #f.close()
    soup = bs(rq.text,"html.parser")
    islogin = soup.find(id="tips")
    if islogin != None:
        return islogin,None,None
    rq = session.get("http://www.zfjw.xupt.edu.cn/jwglxt/xsxxxggl/xsgrxxwh_cxXsgrxx.html?gnmkdm=N100801&layout=default&su=" + yhm)
    soup = bs(rq.text,"html.parser")
    username = soup.find(id= "col_xm").p.text.strip()
    class_name = soup.find(id = 'col_bh_id').p.text.strip()
    return islogin,username,class_name


class ImageCodeView(View):
    def get(self,request):
        '''
        1接收前端传递过来的uuid
        2判断uuid是否获取到
        3通过调用captcha来生成图片验证码（图片二进制和图片内容）
        4将图片内容保存到redis中 uuid-key，图片内容-value，同时设置一个时效
        5返回图片二进制
        :param request:
        :return:
        '''
        uuid = request.GET.get('uuid')
        if uuid is None:
            return HttpResponseBadRequest('没有传递uuid')
        text,image = captcha.generate_captcha()
        redis_conn = get_redis_connection('default')
        #uuid 过期秒数 图片二进制内容
        redis_conn.setex('img:%s'%uuid,300,text)
        return HttpResponse(image,content_type='image/jpeg')

class SmsCodeView(View):
    """
    1.接收参数
    2.参数的验证
        2.1 验证参数是否齐全
        2.2 图片验证码的验证
            连接redis，获取redis中的图片验证码
            判断图片验证码是否存在
            如果图片验证码未过期，我们获取到之后就可以删除图片验证码
            比对图片验证码
    3.生成短信验证码
    4.保存短信验证码到redis中
    5.发送短信
    6.返回响应
    :param request:
    :return:
    """
    def get(self,request):
        # 接收参数
        image_code_client = request.GET.get('image_code')
        uuid = request.GET.get('uuid')
        mobile=request.GET.get('mobile')

        # 校验参数
        if not all([image_code_client, uuid,mobile]):
            return JsonResponse({'code': RETCODE.NECESSARYPARAMERR, 'errmsg': '缺少必传参数'})

        # 创建连接到redis的对象
        redis_conn = get_redis_connection('default')
        # 提取图形验证码
        image_code_server = redis_conn.get('img:%s' % uuid)
        if image_code_server is None:
            # 图形验证码过期或者不存在
            return JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图形验证码失效'})
        # 删除图形验证码，避免恶意测试图形验证码
        try:
            redis_conn.delete('img:%s' % uuid)
        except Exception as e:
            logger.error(e)
        # 对比图形验证码
        image_code_server = image_code_server.decode()  # bytes转字符串
        if image_code_client.lower() != image_code_server.lower():  # 转小写后比较
            return JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '输入图形验证码有误'})

        # 生成短信验证码：生成6位数验证码
        sms_code = '%06d' % randint(0, 999999)
        #将验证码输出在控制台，以方便调试
        logger.info(sms_code)
        # 保存短信验证码到redis中，并设置有效期
        redis_conn.setex('sms:%s' % mobile, 300, sms_code)
        # 发送短信验证码
        template1 = {
            'code': sms_code,
        }
        issend = send_sms(template1,mobile)
        logger.info(issend)

        # 响应结果
        return JsonResponse({'code': RETCODE.OK, 'errmsg': '发送短信成功'})

import re
from users.models import User
from django.db import DatabaseError

class RegisterView(View):
    def get(self,request):
        std_no = request.session.get('std_no', None)
        class_name = request.session.get('class_name', None)
        username = request.session.get('username', None)
        if not std_no:
            return redirect(reverse('users:login'))
        else:
            from django.contrib.auth import authenticate
            user=authenticate(std_no=std_no,password=123)
            if user is None:
                return render(request,'register.html',{'std_no':std_no, 'class_name':class_name, 'username':username})
            else:
                return redirect(reverse('users:center'))

    def post(self,request):
        """
        1.接收数据
        2.验证数据
            2.1 参数是否齐全
            2.2 手机号的格式是否正确
            2.3 密码是否符合格式
            2.4 密码和确认密码要一致
            2.5 短信验证码是否和redis中的一致
        3.保存注册信息
        4.返回响应跳转到指定页面
        :param request:
        :return:
        """
        #接收参数
        std_no = request.POST.get('std_no')
        username = request.POST.get('username')
        class_name = request.POST.get('class_name')
        mobile = request.POST.get('mobile')
        #password = request.POST.get('password')
        #password2 = request.POST.get('password2')
        smscode=request.POST.get('sms_code')
        logger.info(username)
        logger.info(std_no)
        logger.info(class_name)	

        # 判断参数是否齐全
        if not all([mobile, class_name, smscode]):
            return HttpResponseBadRequest('缺少必传参数')
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseBadRequest('请输入正确的手机号码')
        # # 判断密码是否是8-20个数字
        # if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
        #     return HttpResponseBadRequest('请输入8-20位的密码')
        # # 判断两次密码是否一致
        # if password != password2:
        #     return HttpResponseBadRequest('两次输入的密码不一致')


        #验证短信验证码
        redis_conn = get_redis_connection('default')
        sms_code_server = redis_conn.get('sms:%s' % mobile)
        if sms_code_server is None:
            return HttpResponseBadRequest('短信验证码已过期')
        if smscode != sms_code_server.decode():
            return HttpResponseBadRequest('短信验证码错误')

        # 保存注册数据
        try:
            user=User.objects.create_user(username=username, mobile=mobile, class_name=class_name,std_no=std_no,password=123)
        except DatabaseError as de:
            logger.info(de)
            return HttpResponseBadRequest('报名失败')

        from django.contrib.auth import login
        login(request, user)
        # request.session['std_no'] = std_no
        # request.session.set_expiry(600)

        # 响应注册结果
        # redirect 是进行重定向
        # reverse 是可以通过 namespace:name 来获取到视图所对应的路由
        response = redirect(reverse('users:center'))
        # return HttpResponse('注册成功，重定向到首页')

            # 设置cookie信息，以方便首页中 用户信息展示的判断和用户信息的展示
        response.set_cookie('is_login', True,max_age=600)
        # response.set_signed_cookie('std_no', std_no,salt='zion', max_age=600)
        return response





class LoginView(View):

    def get(self,request):
        std_no = request.get_signed_cookie('std_no',None,salt='zion')


#        print(std_no)
        if std_no:
            if request.COOKIES.get('is_login',None) != None:
                return redirect(reverse('users:center'))
            return render(request,'login.html',{'std_no':std_no} )	
        else:
            return render(request,'login.html')

    def post(self,request):
        """
        1.接收参数
        2.参数的验证
            2.1 验证手机号是否符合规则
            2.2 验证密码是否符合规则
        3.用户认证登录
        4.状态的保持
        5.根据用户选择的是否记住登录状态来进行判断
        6.为了首页显示我们需要设置一些cookie信息
        7.返回响应
        :param request:
        :return:
        """
        # 1.接收参数
        #mobile=request.POST.get('mobile')
        receive_data = json.loads(request.body.decode())
        # std_no = request.POST.get('std_no')
        # password=request.POST.get('password')
        std_no = receive_data['id']
        password = receive_data['pwd']

        logger.info("?")
        logger.info(password)
#        remember=request.POST.get('remember')
        # 2.参数的验证
        #     2.1 验证手机号是否符合规则
        #if not re.match(r'^\d{8}$',std_no):
        #    return HttpResponseBadRequest('学号不符合规则')
        #     2.2 验证密码是否符合规则
        #if not re.match(r'^[a-zA-Z0-9]{4,20}$',password):
        #    return HttpResponseBadRequest('密码不符合规则')
        # 3.用户认证登录
        # 采用系统自带的认证方法进行认证
        # 如果我们的用户名和密码正确，会返回user
        # 如果我们的用户名或密码不正确，会返回None
 #       from django.contrib.auth import authenticate
        # 默认的认证方法是 针对于 username 字段进行用户名的判断
        # 当前的判断信息是 手机号，所以我们需要修改一下认证字段
        # 我们需要到User模型中进行修改，等测试出现问题的时候，我们再修改
  #      user=authenticate(mobile=mobile,password=password)

       # if user is None:
        #    return HttpResponseBadRequest('用户名或密码错误')
        # 4.状态的保持
 #       from django.contrib.auth import login
  #      login(request,user)
        # 5.根据用户选择的是否记住登录状态来进行判断
        # 6.为了首页显示我们需要设置一些cookie信息

        #根据next参数来进行页面的跳转
        #next_page=request.GET.get('next')
        islogin,username,class_name = check(std_no,password)

        logger.info(username)
        logger.info(std_no)
        logger.info(class_name)

        if islogin != None:
            return  HttpResponse(json.dumps({'status':'id-pwd-error'}), content_type="application/json")
        else:
            #if next_page:
             #   response=redirect(next_page)

            from django.contrib.auth import authenticate
            user=authenticate(std_no=std_no,password=123)
            if user is None:
            #如果已经报名，跳转至主页
            #如果没有报名，跳转至register
                #response=redirect(reverse('users:register'))
                response=HttpResponse(json.dumps({'status':'200'}), content_type="application/json")
            else:
                #from django.contrib.auth import login
                #login(request, user)
                #response=redirect(reverse('users:center'))
                #response.set_cookie('is_login',True,max_age=600)
                return HttpResponse(json.dumps({'status':'302'}), content_type="application/json")
            request.session['std_no'] = std_no
            request.session['class_name'] = class_name
            request.session['username'] = username
            request.session.set_expiry(600)

            response.set_signed_cookie('std_no',std_no,salt='zion',max_age=600)

#        if remember != 'on':  #没有记住用户信息
#            #浏览器关闭之后
#            request.session.set_expiry(0)
#            response.set_cookie('is_login',True)
#            response.set_cookie('std_no',user.std_no,max_age=14*24*3600)
#        else:                 # 记住用户信息
#            # 默认是记住 2周
#            request.session.set_expiry(None)
#            response.set_cookie('is_login',True,max_age=14*24*3600)
#            response.set_cookie('std_no',user.std_no,max_age=14*24*3600)
#
        # 7.返回响应
        return response

from django.contrib.auth import logout
class LogoutView(View):
    #删除当前登入者的session中的信息

    def get(self,request):
        del request.session['std_no']
        logout(request)
        #重定向至登入界面
        res=redirect(reverse('users:login'))
        res.delete_cookie('is_login')
        return res

from django.contrib.auth.mixins import LoginRequiredMixin
class UserCenterView(LoginRequiredMixin,View):
    def get(self,request):
        # 获得登录用户的信息
        user=request.user
        #组织获取用户的信息
        context = {
            'username':user.username,
            'std_no':user.std_no,
            'class_name':user.class_name
        }
        return render(request,'center.html',context=context)



