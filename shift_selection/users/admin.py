# users/admin.py
from django.contrib import admin
from .models import UserProfile, Shift, Availability, Address, ShiftOffer

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_employer', 'subscription_valid_until', 'subscription_enabled')
    list_filter = ('is_employer', 'subscription_enabled')

admin.site.register(UserProfile, UserProfileAdmin)

class ShiftAdmin(admin.ModelAdmin):
    list_display = ('your_existing_fields', 'max_users')
    # Add other configurations or fields you want to display

admin.site.register(Shift, ShiftAdmin)

class AvailabilityAdmin(admin.ModelAdmin):
    # Customize as needed
    pass

admin.site.register(Availability, AvailabilityAdmin)

class AddressAdmin(admin.ModelAdmin):
    # Customize as needed
    pass

admin.site.register(Address, AddressAdmin)

class ShiftOfferAdmin(admin.ModelAdmin):
    # Customize as needed
    pass

admin.site.register(ShiftOffer, ShiftOfferAdmin)
