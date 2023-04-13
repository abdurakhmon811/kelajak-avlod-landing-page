from django.contrib import admin
from .models import Book, IndexInfo
from .relations import SocialMedia


admin.site.register([Book, IndexInfo, SocialMedia])
