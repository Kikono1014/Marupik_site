# Generated by Django 3.2.3 on 2021-06-20 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='mayor',
            field=models.CharField(default='ananist', max_length=100),
        ),
    ]
