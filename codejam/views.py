from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RegisterForm, ReservationForm
from django.contrib.auth.decorators import login_required
from .models import CommonSpace, Reservation
from django.core.exceptions import ValidationError


def index(req):
    return render(req,"landing.html")

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RegisterForm

def login_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            # Autenticar y loguear al usuario
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, f'Account created for {username}!')
            return redirect('home')  # Redirigir a la página de inicio u otra página deseada
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})



@login_required
def reservation_list(request):
    reservations = Reservation.objects.all()
    #reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'reservation_list.html', {'reservations': reservations})

# @login_required
# def reservation_create(request):
#     if request.method == 'POST':
#         form = ReservationForm(request.POST)
#         if form.is_valid():
#             reservation = form.save(commit=False)
#             reservation.user = request.user
#             reservation.save()
#             return redirect('reservation_list')
#     else:
#         form = ReservationForm()
#     return render(request, 'reservation_form.html', {'form': form})

@login_required
def reservation_create(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            try:
                reservation.save()
                return redirect('reservation_list')
            except ValidationError as e:
                form.add_error(None, e.message)
    else:
        form = ReservationForm()
    return render(request, 'reservation_form.html', {'form': form})

@login_required
def cancel_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if reservation.user == request.user:
        reservation.delete()
        return redirect('reservation_list')  # Redirige a la lista de reservas o a la página que prefieras
    else:
        return redirect('reservation_list')  # Redirige a la lista de reservas o muestra un mensaje de error