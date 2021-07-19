from django.contrib import admin

from .models import Profile, News, Article, City, Penetration, NewsComment, UserComment, ArticleComment


admin.site.register(Profile)
admin.site.register(News)
admin.site.register(Article)
admin.site.register(City)
admin.site.register(Penetration)
admin.site.register(NewsComment)
admin.site.register(UserComment)
admin.site.register(ArticleComment)