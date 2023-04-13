from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Client


class ClientCreationForm(forms.ModelForm):
    """
    A form for creating a new client user.
    """

    class Meta:
        model = Client
        fields = '__all__'
    

    def save(self, commit=True):

        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class ClientChangeForm(forms.ModelForm):
    """
    A form for changing the client data.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Client
        fields = '__all__'
    

class ClientAdmin(BaseUserAdmin):
    """
    A model of admin for managing clients.
    """

    form = ClientChangeForm
    add_form = ClientCreationForm

    list_display = ('names', 'phone_number')
    list_filter = (
        'is_superuser',
    )
    fieldsets = (
        (
            None, 
            {
                'fields': ['names', 'phone_number', 'password'],
            },
        ),
        (
            'Client information', 
            {
                'fields': ['address', 'email', 'childs_class'],
            },
        ),
        (
            'Server-side properties',
            {
                'fields': ['is_active', 'is_admin', 'is_staff', 'is_superuser', 'last_login', 'date_joined'],
            }
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ['names', 'phone_number', 'password'],
            },
        ),
        (
            'Client information',
            {
                'classes': ('wide',),
                'fields': ['address', 'email', 'childs_class'],
            }
        ),
        (
            'Server-side properties',
            {
                'classes': ('wide',),
                'fields': ['is_active', 'is_admin', 'is_staff', 'is_superuser', 'last_login', 'date_joined'],
            }
        ),
    )

    search_fields = ('names', 'phone_number', 'email')
    ordering = (
        'names',
    )
    filter_horizontal = ()
