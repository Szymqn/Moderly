from django import forms
from .models import Comment, Product


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    parent = forms.ModelChoiceField(queryset=Comment.objects.all(), required=False, widget=forms.HiddenInput())


class ProductDescriptionForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 10,
                'cols': 120,
            },),
        }
