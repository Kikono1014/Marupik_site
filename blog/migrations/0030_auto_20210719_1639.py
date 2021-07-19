# Generated by Django 3.2.3 on 2021-07-19 13:39

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0029_auto_20210719_1524'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='article/image/')),
                ('title', models.CharField(max_length=1000)),
                ('text', models.TextField()),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('active', models.BooleanField(default=True)),
                ('author', models.CharField(default='ananist', max_length=100)),
            ],
        ),
        migrations.RenameModel(
            old_name='Comment',
            new_name='NewsComment',
        ),
        migrations.CreateModel(
            name='ArticleComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(default='none', max_length=300)),
                ('name', models.CharField(max_length=100)),
                ('userid', models.CharField(default=3, max_length=1000)),
                ('role', models.CharField(default='Игрок', max_length=100)),
                ('body', models.TextField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('active', models.BooleanField(default=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.article')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]
