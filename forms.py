# -*- coding: utf-8 -*-
from django import forms
from .models import Profile, News, City, Penetration, Comment, UserComment
from django.contrib.auth.models import User

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('body',)
	
class UserCommentForm(forms.ModelForm):
	class Meta:
		model = UserComment
		fields = ('body',)
	

class EditCommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('body',)

class DeleteCommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = []

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

class Add_nuwsForm(forms.ModelForm):
	class Meta:
		model = News
		fields = ('image', 'title', 'text',)

class Add_citeForm(forms.ModelForm):
	class Meta:
		model = City
		fields = ('image', 'image1', 'image2', 'image3', 'image4', 'image5', 'title', 'text', 'smol_text', 'contact_url', 'mayor')

class PenetrationForm(forms.ModelForm):
	class Meta:
		model = Penetration
		fields = ('minecraft_nickname', 'donation_username', 'free_token', 'donation_image', 'description_yourself', 'how_you_know', 'contact', 'status')
class EditPenetrationForm(forms.ModelForm):
	class Meta:
		model = Penetration
		fields = ('status',)

