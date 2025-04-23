from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    # Добавляем 'subject' в list_display
    list_display = ('name', 'email', 'message', 'subject', 'submitted_at')

    # Добавляем 'subject' в readonly_fields
    readonly_fields = ('name', 'email', 'message', 'subject', 'submitted_at')

    # Устанавливаем порядок отображения
    ordering = ('-submitted_at',)




