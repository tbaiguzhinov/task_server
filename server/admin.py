from django.contrib import admin
from server.models import ErrorLog


@admin.register(ErrorLog)
class ErrorLogAdmin(admin.ModelAdmin):
    pass
