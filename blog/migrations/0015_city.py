# Generated by Django 3.2.3 on 2021-06-20 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_alter_news_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='city/image/')),
                ('title', models.CharField(max_length=100)),
                ('smol_text', models.TextField(max_length=1000)),
                ('text', models.TextField(max_length=100)),
                ('contact_url', models.URLField()),
                ('active', models.BooleanField(default=True)),
                ('author', models.CharField(default='ananist', max_length=100)),
            ],
        ),
    ]
