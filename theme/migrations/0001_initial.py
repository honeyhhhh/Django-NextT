# Generated by Django 3.1.1 on 2020-09-23 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='welcome', max_length=20, verbose_name='站点标题')),
                ('home_title', models.CharField(default='DjangoBlog', max_length=20, verbose_name='主页标题')),
                ('home_title_down', models.CharField(default='use Theme NextT', max_length=20, verbose_name='主页副标题')),
                ('nick_name', models.CharField(default='username', max_length=20, verbose_name='昵称')),
                ('head_image', models.ImageField(upload_to='head_image', verbose_name='用户头像(≤512x512)')),
                ('introduction', models.CharField(default='hello world', max_length=50, verbose_name='简介')),
                ('email', models.EmailField(blank=True, max_length=50, null=True, verbose_name='邮箱')),
                ('github', models.CharField(blank=True, max_length=20, null=True, verbose_name='Github 用户名')),
                ('csdn', models.CharField(blank=True, max_length=100, null=True, verbose_name='CSDN ID号')),
                ('beian', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='备案号')),
                ('music', models.CharField(default='28692687', max_length=20, verbose_name='网易云歌曲 ID')),
                ('live2d', models.CharField(choices=[('o', '打开'), ('c', '关闭')], default='c', max_length=1, verbose_name='live2d开启')),
            ],
            options={
                'verbose_name': '主题配置',
                'verbose_name_plural': '主题配置',
            },
        ),
    ]
