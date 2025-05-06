# Register your models here.
from django.contrib import admin
from .models import ContactMessage
from .models import Recipe, Category


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    # Добавляем 'subject' в list_display
    list_display = ('name', 'email', 'message', 'subject', 'submitted_at')

    # Добавляем 'subject' в readonly_fields
    readonly_fields = ('name', 'email', 'message', 'subject', 'submitted_at')

    # Устанавливаем порядок отображения
    ordering = ('-submitted_at',)

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at')  # Что будет отображаться в таблице
    search_fields = ('title', 'author__username', 'category__name')  # Поля для поиска
    list_filter = ('category', 'created_at')  # Фильтры для списка рецептов

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Category)