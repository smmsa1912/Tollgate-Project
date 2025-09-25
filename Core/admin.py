from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("First_Name", "Last_Name", "Email", "Phone_Number")
    list_filter = ["is_active"]
    readonly_fields = ("password", )
    search_fields = ["First_Name", "Last_Name", "Email", "Phone_Number", "Car_Number", "RFID"]
    ordering = ["First_Name", "Last_Name"]
    fieldsets = [
        ("User Information",
         {"fields": ["RFID", "Car_Number", "First_Name", "Last_Name", "Email", "Phone_Number", "password"]}),
        ("Permissions", {"fields": ["is_superuser", "is_staff", "is_active"]}),
    ]