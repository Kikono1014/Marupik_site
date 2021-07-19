# -*- coding: utf-8 -*-
from django import forms
from .models import Profile, News, Article, City, Penetration, NewsComment, UserComment, ArticleComment
from django.contrib.auth.models import User


class NewsCommentForm(forms.ModelForm):
    class Meta:
        model = NewsComment
        fields = ('body',)

class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = ArticleComment
        fields = ('body',)


class Add_nuwsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('image', 'title', 'text',)

class DeleteNewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = []


class DeleteArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = []


class EditNewsCommentForm(forms.ModelForm):
    class Meta:
        model = NewsComment
        fields = ('body',)


class DeleteNewsCommentForm(forms.ModelForm):
    class Meta:
        model = NewsComment
        fields = []


class NewsArticleForm(forms.ModelForm):
    class Meta:
        model = ArticleComment
        fields = ('body',)


class AddArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('image', 'title', 'text',)


class EditArticleCommentForm(forms.ModelForm):
    class Meta:
        model = NewsComment
        fields = ('body',)


class DeleteArticleCommentForm(forms.ModelForm):
    class Meta:
        model = NewsComment
        fields = []


class UserCommentForm(forms.ModelForm):
    class Meta:
        model = UserComment
        fields = ('body',)

class DeleteUserCommentForm(forms.ModelForm):
    class Meta:
        model = UserComment
        fields = []


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('user_image', 'info',)




class Add_citeForm(forms.ModelForm):
    class Meta:
        model = City
        fields = (
            'image',
            'image1',
            'image2',
            'image3',
            'image4',
            'image5',
            'title',
            'text',
            'smol_text',
            'contact_url',
            'mayor'
        )


class PenetrationForm(forms.ModelForm):
    class Meta:
        model = Penetration
        fields = (
            'minecraft_nickname',
            'donation_username',
            'free_token',
            'donation_image',
            'description_yourself',
            'how_you_know',
            'contact',
            'status'
        )


class EditPenetrationForm(forms.ModelForm):
    class Meta:
        model = Penetration
        fields = ('status',)
