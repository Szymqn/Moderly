from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    parent = forms.ModelChoiceField(queryset=Comment.objects.all(), required=False, widget=forms.HiddenInput())
