# Generated by Django 3.2.3 on 2021-06-20 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_news_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='author',
            field=models.CharField(default='ananist', max_length=100),
        ),
    ]
