from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from . models import Post, Comment, Profile
from django import forms
from django.forms import ModelForm

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title','post',)
        labels = {
            'title': _('Post title')
        }
        widgets = {
            'title': forms.TextInput(
				attrs={
                    'class': 'form-control mb-3',
                    'placeholder': 'title of your post'
                }),
            'post': forms.Textarea(
				attrs={
                    'class': 'form-control mb-3',
                    'rows': 8,
                    'placeholder': 'write your post'
                }),
			}

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
        labels = {
            'comment': _('')
        }
        widgets = {
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control mb-3',
                    'rows': 4,
                    'placeholder': 'write your comment'
                }
            )
        }

class UpdateProfile(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email',)

        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control'

                }
            ),

            'email': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            )
        }

class UpdateProfilePic(ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_pic',)