from django import forms
from .models import CartItem


class AddToCartForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']


class CheckoutForm(forms.Form):
    street_address = forms.CharField(max_length=100, required=False)
    city = forms.CharField(max_length=50, required=False)
    state = forms.CharField(max_length=50, required=False)
    postal_code = forms.CharField(max_length=10, required=False)
    country = forms.CharField(max_length=50, required=False)
    payment_method = forms.ChoiceField(choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal')], required=False)
