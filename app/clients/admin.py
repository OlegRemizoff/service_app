from django.contrib import admin
from .models import Client



@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'company_name']
    list_display_links =['id', 'user']




