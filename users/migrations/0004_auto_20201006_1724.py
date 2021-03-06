# Generated by Django 3.0.8 on 2020-10-06 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20201006_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='class_name',
            field=models.CharField(max_length=20, verbose_name='班级'),
        ),
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.CharField(max_length=20, unique=True, verbose_name='电话'),
        ),
        migrations.AlterField(
            model_name='user',
            name='std_no',
            field=models.CharField(max_length=10, unique=True, verbose_name='学号'),
        ),
    ]
