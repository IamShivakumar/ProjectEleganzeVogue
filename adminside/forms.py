from django import forms
from .models import coupon

class CouponForm(forms.ModelForm):
    class Meta:
        model = coupon
        fields = ['code','description', 'discount']

