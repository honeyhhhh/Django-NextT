# Generated by Django 3.0.8 on 2020-10-20 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20201020_2131'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagname', models.CharField(max_length=100, verbose_name='文章标签')),
            ],
        ),
        migrations.RemoveField(
            model_name='article',
            name='author',
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='home.Tag'),
        ),
    ]
