# Generated by Django 3.2.3 on 2021-06-17 17:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_news_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='users/image/')),
                ('username', models.CharField(max_length=50)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('role', models.TextField(default='Игрок')),
                ('admin', models.BooleanField(default=False)),
            ],
        ),
    ]
