# Generated by Django 3.2.3 on 2021-06-22 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_auto_20210622_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='penetration',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
