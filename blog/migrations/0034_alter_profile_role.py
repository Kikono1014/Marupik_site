# Generated by Django 3.2.3 on 2021-07-20 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0033_auto_20210720_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('Игрок', 'Игрок'), ('Журналист', 'Журналист'), ('Мэр', 'Мэр'), ('Президент', 'Президент'), ('ФБР', 'ФБР'), ('Глава ФБР', 'Глава ФБР')], default=None, max_length=9, null=True, verbose_name='Do you own a Smartphone?'),
        ),
    ]