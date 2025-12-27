from django import forms
from events.models import SeatType


class BookingForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'min': 1,
                'inputmode': 'numeric',
                'placeholder': 'Enter number of tickets'
            }
        )
    )

    seat_type = forms.ModelChoiceField(
        queryset=SeatType.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Seat Type'
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

    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event', None)
        super().__init__(*args, **kwargs)
        if event is not None:
            self.fields['seat_type'].queryset = event.seat_types.all()

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity < 1:
            raise forms.ValidationError('Quantity must be at least 1.')
        # No upper limit here
        return quantity
