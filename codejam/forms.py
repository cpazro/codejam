from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Reservation
from datetime import timedelta
#comentario ds

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['common_space', 'start_time', 'end_time', 'purpose']
        widgets = {
            'common_space': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'purpose': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        common_space = cleaned_data.get('common_space')
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if end_time and start_time and end_time > start_time + timedelta(hours=4):
            raise forms.ValidationError("end_time must be within 4 hours of start_time")
        
        if start_time and end_time:
            overlapping_reservations = Reservation.objects.filter(
                common_space=common_space,
                start_time__lt=end_time,
                end_time__gt=start_time
            )
            if overlapping_reservations.exists():
                f"Ya hay una reserva para este periodo de tiempo: "
                
        
        return cleaned_data    

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

