from django import forms
from .models import userAddress

class AddressForm(forms.ModelForm):
    class Meta:
        model = userAddress
        fields = ['name','house_no', 'street', 'state', 'city', 'pincode', 'is_primary']

