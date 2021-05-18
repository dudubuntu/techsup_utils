from django.contrib import admin
from utilsapp.models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    fields = ['name', 'created', 'file']
    list_display = ['name', 'created', 'file']
    readonly_fields = ['created']