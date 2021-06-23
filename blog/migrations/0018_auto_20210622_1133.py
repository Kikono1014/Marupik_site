# Generated by Django 3.2.3 on 2021-06-22 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_auto_20210621_2136'),
    ]

    operations = [
        migrations.CreateModel(
            name='Penetration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minecraft_nickname', models.CharField(default='Не указано', max_length=100)),
                ('site_username', models.CharField(default='Не указано', max_length=100)),
                ('donation_username', models.CharField(default='Не указано', max_length=100)),
                ('free_token', models.CharField(default='Не указано', max_length=300)),
                ('donation_image', models.ImageField(blank=True, default='penetration/image/default/default.png', upload_to='penetration/image/')),
                ('description_yourself', models.TextField(default='Не описано.')),
                ('how_you_know', models.TextField(default='Не описано.', max_length=400)),
                ('contact', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='registered',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='city',
            name='smol_text',
            field=models.TextField(default='Информация от мэра города не поступила.', max_length=400),
        ),
        migrations.AlterField(
            model_name='city',
            name='text',
            field=models.TextField(default='Информация от мэра города не поступила.'),
        ),
    ]
