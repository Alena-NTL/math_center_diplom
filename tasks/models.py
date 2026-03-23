from django.db import models
from django.conf import settings


class Subject(models.Model):
    """Предмет: Алгебра, Геометрия..."""
    name = models.CharField('Название', max_length=100)
    sort_order = models.PositiveIntegerField('Порядок сортировки', default=0)

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name


class Topic(models.Model):
    """Тема: Квадратные уравнения, Теорема Пифагора..."""
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='topics',
        verbose_name='Предмет',
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Родительская тема',
    )
    name = models.CharField('Название', max_length=200)
    grade = models.PositiveIntegerField('Класс (5-11)')
    sort_order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'
        ordering = ['grade', 'sort_order', 'name']

    def __str__(self):
        return f'{self.name} ({self.grade} кл.)'


class DifficultyLevel(models.Model):
    """Уровень сложности."""
    name = models.CharField('Название', max_length=50)
    numeric_value = models.PositiveIntegerField(
        'Числовое значение',
        help_text='1 — лёгкий, 2 — средний, 3 — сложный, 4 — олимпиадный',
    )

    class Meta:
        verbose_name = 'Уровень сложности'
        verbose_name_plural = 'Уровни сложности'
        ordering = ['numeric_value']

    def __str__(self):
        return self.name


class Task(models.Model):
    """Задача в банке задач."""

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Черновик'
        ON_REVIEW = 'on_review', 'На рассмотрении'
        APPROVED = 'approved', 'Одобрена'
        REJECTED = 'rejected', 'Отклонена'
        REVISION = 'revision', 'На доработке'

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='Автор',
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.PROTECT,
        related_name='tasks',
        verbose_name='Тема',
    )
    difficulty = models.ForeignKey(
        DifficultyLevel,
        on_delete=models.PROTECT,
        related_name='tasks',
        verbose_name='Сложность',
    )
    body = models.TextField(
        'Текст задачи',
        help_text='Для формул используйте LaTeX: $x^2 + 3x = 0$',
    )
    answer = models.TextField('Ответ')
    solution = models.TextField('Решение', blank=True)
    status = models.CharField(
        'Статус',
        max_length=15,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    created_at = models.DateTimeField('Создана', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлена', auto_now=True)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-created_at']

    def __str__(self):
        return f'Задача #{self.pk}: {self.body[:50]}...'


class TaskImage(models.Model):
    """Изображение к задаче."""
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Задача',
    )
    image = models.ImageField('Изображение', upload_to='task_images/%Y/%m/')
    caption = models.CharField('Подпись', max_length=200, blank=True)
    sort_order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ['sort_order']

    def __str__(self):
        return f'Изображение к задаче #{self.task.pk}'
