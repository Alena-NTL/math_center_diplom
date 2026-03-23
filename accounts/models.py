from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Пользователь системы с ролью."""

    class Role(models.TextChoices):
        ADMIN = 'admin', 'Администратор'
        TEACHER = 'teacher', 'Преподаватель'

    role = models.CharField(
        'Роль',
        max_length=10,
        choices=Role.choices,
        default=Role.TEACHER,
    )
    patronymic = models.CharField(
        'Отчество',
        max_length=150,
        blank=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.last_name} {self.first_name} ({self.get_role_display()})'

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN

    @property
    def is_teacher(self):
        return self.role == self.Role.TEACHER

