# Generated by Django 3.0.8 on 2020-10-20 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20201020_1415'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='文章标签')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='tags2',
            field=models.ManyToManyField(blank=True, to='home.Tag2'),
        ),
    ]
