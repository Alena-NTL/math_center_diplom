from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'last_name', 'first_name', 'role', 'is_active')
    list_filter = ('role', 'is_active')

    # Добавляем наши поля в форму редактирования
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('role', 'patronymic')}),
    )

    # Добавляем наши поля в форму создания
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительно', {'fields': ('role', 'first_name', 'last_name', 'patronymic')}),
    )

