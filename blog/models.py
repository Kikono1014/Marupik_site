from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class News(models.Model):
    image = models.ImageField(
        upload_to='news/image/',
        height_field=None,
        width_field=None,
        max_length=100
    )
    title = models.CharField(max_length=1000)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    pyblished_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    author = models.CharField(max_length=100, default="ananist")

    def publish(self):
        self.publish_date = timezone.now()


class NewsComment(models.Model):
    news = models.ForeignKey(
        News, related_name='comments', on_delete=models.CASCADE
    )
    image = models.CharField(max_length=300, default="none")
    name = models.CharField(max_length=100)
    userid = models.CharField(max_length=1000, default=3)
    role = models.CharField(max_length=100, default="Игрок")
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)


class Article(models.Model):
    image = models.ImageField(
        upload_to='article/image/',
        height_field=None,
        width_field=None,
        max_length=100
    )
    title = models.CharField(max_length=1000)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    author = models.CharField(max_length=100, default="ananist")



class ArticleComment(models.Model):
    article = models.ForeignKey(
        Article, related_name='comments', on_delete=models.CASCADE
    )
    image = models.CharField(max_length=300, default="none")
    name = models.CharField(max_length=100)
    userid = models.CharField(max_length=1000, default=3)
    role = models.CharField(max_length=100, default="Игрок")
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

class UserComment(models.Model):
    user = models.ForeignKey(
        User, related_name='comments', on_delete=models.CASCADE
    )
    image = models.CharField(max_length=300, default="none")
    name = models.CharField(max_length=100)
    userid = models.CharField(max_length=1000, default=3)
    role = models.CharField(max_length=100, default="Игрок")
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)


class Profile(models.Model):
    role1 = 'Игрок'
    role2 = 'Журналист'
    role3 = 'Мэр'
    role4 = 'Президент'
    role5 = 'ФБР'
    role6 = 'Глава ФБР'
    ROLES = [
        (role1, 'Игрок'),
        (role2, 'Журналист'),
        (role3, 'Мэр'),
        (role4, 'Президент'),
        (role5, 'ФБР'),
        (role6, 'Глава ФБР'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_image = models.ImageField(
        upload_to='users/user_image/',
        default="users/user_image/default/default.png",
        blank=True
    )

    info = models.TextField(
        default='Проходивший мимо пользователь сайта,'
        'который ничего о себе не написал',
        max_length=1000
    )

    create_date = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=9, choices=ROLES, default=role1)
    unconfirmed_discord = models.CharField(max_length=100, default="Не задан")
    unconfirmed_discord = models.CharField(max_length=100, default="Не задан")
    admin = models.BooleanField(default=False)
    registered = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class City(models.Model):
    status1 = 'Открыт'
    status2 = 'Закрыт'
    status3 = 'Не функционирует'
    STATUS = [
        (status1, 'Открыт'),
        (status2, 'Закрыт'),
        (status3, 'Не функционирует'),
    ]

    image = models.ImageField(
        default="city/image/default/default.png",
        upload_to='city/image/',
        max_length=100,
        blank=True
    )
    image2 = models.ImageField(
        default="city/image/default/default.png",
        upload_to='city/image/',
        max_length=100,
        blank=True
    )
    image1 = models.ImageField(
        default="city/image/default/default.png",
        upload_to='city/image/',
        max_length=100,
        blank=True
    )
    image3 = models.ImageField(
        default="city/image/default/default.png",
        upload_to='city/image/',
        max_length=100,
        blank=True
    )
    image4 = models.ImageField(
        default="city/image/default/default.png",
        upload_to='city/image/',
        max_length=100,
        blank=True
    )
    image5 = models.ImageField(
        default="city/image/default/default.png",
        upload_to='city/image/',
        max_length=100,
        blank=True
    )

    title = models.CharField(max_length=100)
    smol_text = models.TextField(
        max_length=400,
        default="Информация от мэра города не поступила."
    )
    text = models.TextField(
        default="Информация от мэра города не поступила."
    )
    status = models.CharField(max_length=17, choices=STATUS, default=status1)
    contact_url = models.URLField()
    active = models.BooleanField(default=True)
    author = models.CharField(max_length=100, default="ananist")
    mayor = models.CharField(max_length=100, default="ananist")


class Penetration(models.Model):
    minecraft_nickname = models.CharField(max_length=100, default="Не указано")
    site_username = models.CharField(max_length=100, default="Не указано")
    donation_username = models.CharField(max_length=100, default="Не указано")
    free_token = models.CharField(max_length=300, default="Не указано")
    donation_image = models.ImageField(
        default="penetration/image/default/default.png",
        upload_to='penetration/image/',
        max_length=100,
        blank=True
    )
    description_yourself = models.TextField(default="Не описано.")
    how_you_know = models.TextField(default="Не описано.")
    contact = models.CharField(max_length=200)
    status = models.BooleanField(default=False)
    create_date = models.DateTimeField(default=timezone.now)
