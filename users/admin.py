from django.contrib import admin
from django.contrib.auth.models import Group
from .forms import ClientAdmin
from .models import Client


admin.site.register(Client, ClientAdmin)
admin.site.unregister(Group)