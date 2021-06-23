from django.contrib import admin

from .models import News, Profile, City, Penetration, Comment, UserComment


admin.site.register(Profile)
admin.site.register(News)
admin.site.register(City)
admin.site.register(Penetration)
admin.site.register(Comment)
admin.site.register(UserComment)