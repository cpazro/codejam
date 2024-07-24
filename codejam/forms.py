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
            raise forms.ValidationError("La reserva no puede durar más de 4 horas.")
        
        if start_time and end_time:
            overlapping_reservations = Reservation.objects.filter(
                common_space=common_space,
                start_time__lt=end_time,
                end_time__gt=start_time
            )
            if overlapping_reservations.exists():
                overlapping_reservation = overlapping_reservations.first()
                formatted_start_time = overlapping_reservation.start_time.strftime('%d de %B %H:%M')
                formatted_end_time = overlapping_reservation.end_time.strftime('%H:%M')
                raise forms.ValidationError(
                    f"Ya hay una reserva para este periodo de tiempo "
                    f"en: {overlapping_reservation.common_space} {formatted_start_time} - {formatted_end_time}."
                )
                
        
        return cleaned_data    

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

