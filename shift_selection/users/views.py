# views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.conf import settings
from django.contrib import messages
from stripe.api_resources import customer
from .models import Shift, Availability, Address, ShiftOffer, UserProfile
from .forms import ShiftSelectionForm, ShiftOfferForm

@login_required
def shift_list(request):
    user_profile = UserProfile.objects.get(user=request.user)

    # Check if the employer's subscription is still valid
    if user_profile.is_employer and user_profile.subscription_enabled and (user_profile.subscription_valid_until is None or user_profile.subscription_valid_until < timezone.now().date()):
        # Redirect or show an error page indicating the subscription has expired
        return render(request, 'subscription_expired.html')

    # Check if the subscription module is enabled
    if not user_profile.subscription_enabled:
        # Allow employers to use the service without charge
        # Adjust your logic accordingly, for example, by not performing subscription-related checks
        pass
    else:
        # Continue with subscription-related logic
        if not user_profile.subscription_valid_until:
            return redirect('subscribe')  # Redirect to the payment view

    shifts = Shift.objects.all()
    availabilities = Availability.objects.filter(user=request.user)
    addresses = Address.objects.filter(user=request.user)

    # Find the next available shift
    next_available_shift = None
    for shift in shifts:
        availability = availabilities.filter(shift=shift).first()
        if availability and availability.is_available and shift.start_time > timezone.now():
            # Check if the maximum number of users is reached for the shift
            if availability.user_count() < shift.max_users:
                next_available_shift = shift
                break

    # Handle form submission
    if request.method == 'POST':
        form = ShiftSelectionForm(user=request.user, data=request.POST)
        if form.is_valid():
            selected_shift = form.cleaned_data['selected_shift']
            selected_address = form.cleaned_data['selected_address']
            date_time_selected = form.cleaned_data['date_time_selected']

            # Create or update availability record
            availability, created = Availability.objects.get_or_create(user=request.user, shift=selected_shift, address=selected_address)
            availability.date_time_selected = date_time_selected
            availability.is_available = True  # Set to True as the user is selecting this shift
            availability.save()

            return redirect('shift_list')

    else:
        form = ShiftSelectionForm(user=request.user)

    # Display shift offers
    shift_offers_received = ShiftOffer.objects.filter(user=request.user)
    shift_offers_sent = ShiftOffer.objects.filter(employer=request.user)

    context = {
        'shifts': shifts,
        'availabilities': availabilities,
        'next_available_shift': next_available_shift,
        'form': form,
        'addresses': addresses,
        'shift_offers_received': shift_offers_received,
        'shift_offers_sent': shift_offers_sent,
        'is_group_subscription': user_profile.is_group_subscription,
        'group_subscription_id': user_profile.group_subscription_id,
    }
    return render(request, 'shift_list.html', context)

@login_required
def subscribe(request):
    user_profile = UserProfile.objects.get(user=request.user)

    # Check if the subscription module is enabled
    if not user_profile.subscription_enabled:
        # Allow users to use the service without charge
        # Adjust your logic accordingly, for example, by not creating a Stripe customer or session
        messages.info(request, 'Subscription module is not enabled. You can use the service without charge.')
        return redirect('shift_list')

    if request.method == 'POST':
        # Remaining logic for subscription handling remains the same
        pass

    return render(request, 'subscribe.html')
