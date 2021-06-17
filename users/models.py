from django.db import models
from django.contrib.auth.models import User,AbstractUser
# Create your models here.
from datetime import datetime

class BaseModel(models.Model):
    add_time = models.DateField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        abstract = True

# 用户信息
class User(AbstractUser):

    # 电话号码字段
    # unique 为唯一性字段,blank必须填写
    class_name = models.CharField('班级',max_length=20, unique=False, blank=False) #班级
    mobile = models.CharField('电话',max_length=20, unique=True, blank=False) #电话
    std_no = models.CharField('学号',max_length=10, unique=True, blank=False) #学号
    direction = models.CharField('方向',max_length=10,unique=False,blank=True) #方向


    # # 头像
    # # upload_to为保存到响应的子目录中
    # avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)

    # # 个人简介
    # user_desc = models.TextField(max_length=500, blank=True)

    # 修改认证的字段
    USERNAME_FIELD = 'std_no'

    #创建超级管理员的需要必须输入的字段
    REQUIRED_FIELDS = ['username']

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        db_table='tb_user'              #修改默认的表名
        verbose_name='用户信息'         # Admin后台显示
        verbose_name_plural=verbose_name # Admin后台显示

    def __str__(self):
        return self.mobile
