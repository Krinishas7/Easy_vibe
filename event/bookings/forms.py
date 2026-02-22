from django import forms
from .models import Booking


class BookingForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        max_value=10,
        widget=forms.Select(choices=[(i, f'{i} ticket{"s" if i > 1 else ""}') for i in range(1, 11)],
                          attrs={'class': 'form-select'})
    )
    contact_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'})
    )
    contact_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )
    contact_phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
    )

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity < 1:
            raise forms.ValidationError('Quantity must be at least 1.')
        if quantity > 10:
            raise forms.ValidationError('Maximum 10 tickets per booking.')
        return quantity
