# views.py
from django.shortcuts import render, redirect
from .forms import PhysicianRegistrationForm, NurseRegistrationForm
from .utils import generate_jwt

def register_physician(request):
    if request.method == 'POST':
        form = PhysicianRegistrationForm(request.POST)
        if form.is_valid():
            # Save physician data to the database
            # ...

            # Generate JWT for validation
            jwt_token = generate_jwt()
            return render(request, 'success.html', {'jwt_token': jwt_token})
    else:
        form = PhysicianRegistrationForm()

    return render(request, 'register_physician.html', {'form': form})

def register_nurse(request):
    if request.method == 'POST':
        form = NurseRegistrationForm(request.POST)
        if form.is_valid():
            # Save nurse data to the database
            # ...

            # Generate JWT for validation
            jwt_token = generate_jwt()
            return render(request, 'success.html', {'jwt_token': jwt_token})
    else:
        form = NurseRegistrationForm()

    return render(request, 'register_nurse.html', {'form': form})
