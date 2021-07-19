from django.contrib import admin
from django.urls import path, re_path
from . import views

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
            path('',views.show_main),
            path('main/',views.show_main),
            path('map/',views.show_map),
            path('info/',views.show_info),
            path('register/', views.register),
            path('logout/', views.logout_user, name='logout'),
            path('login/', views.login_user, name='login'),
            path('all_profile/', views.all_profile),

            path('profile/', views.profile),
            path('profile/<int:user_id>/', views.another_profile,  name='another_profile'),
            path('profile/delete/user_comment/<int:user_id>/<int:comment_id>',views.delete_user_comment,  name='user_comment_delete'),
            path('profile/upgrade/', views.upgrade_profile),


            path('news/<int:news_id>/',views.show_one_news,  name='one_news'),
            path('news/add/', views.add_news),
            path('news/edit/<int:news_id>/', views.edit_news,  name='edit_one_news'),
            path('news/delete/comment/<int:news_id>/<int:comment_id>',views.delete_news_comment,  name='news_comment_delete'),
            path('news/edit/comment/<int:news_id>/<int:comment_id>',views.edit_news_comment,  name='news_comment_edit'),
            re_path(r'^news*',views.show_news),

            re_path(r'^cities*',views.show_cities),
            path('city/<int:city_id>/',views.show_one_city,  name='one_city'),
            path('city/add', views.add_city),
            path('city/edit/<int:city_id>/', views.edit_city,  name='edit_one_city'),

            re_path(r'^forms*',views.show_forms),
            path('form/<int:form_id>/',views.show_one_form,  name='one_form'),
            path('form/add/', views.add_form),
            path('form/edit/<int:form_id>/', views.edit_form,  name='edit_one_form'),

            
            path('article/add/', views.add_article),
            path('article/edit/<int:article_id>/', views.edit_article,  name='edit_one_article'),
            path('article/<int:article_id>/',views.show_one_article,  name='one_article'),
            path('article/delete/comment/<int:article_id>/<int:comment_id>',views.delete_article_comment,  name='article_comment_delete'),
            path('article/edit/comment/<int:article_id>/<int:comment_id>',views.edit_article_comment,  name='article_comment_edit'),
            re_path(r'^articles*',views.show_articles),


            



            path('change_theme/colored_purpule_gold', views.colored_purpule_gold_theme),
            path('change_theme/dark', views.dark_theme),
            path('change_theme/light', views.light_theme),

            path('api/', views.api, name="api"),
            path('discord/', views.discord, name="discord"),
            
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
