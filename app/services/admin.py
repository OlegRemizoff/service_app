from django.contrib import admin
from .models import Service, Plan, Subscripton


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscripton)
class AuthorAdmin(admin.ModelAdmin):
    pass