from django.db import models
from django.conf import settings


class Assignment(models.Model):
    """Домашнее задание."""
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name='Создал',
    )
    title = models.CharField('Название', max_length=200)
    grade = models.PositiveIntegerField('Класс', null=True, blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Домашнее задание'
        verbose_name_plural = 'Домашние задания'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class AssignmentTask(models.Model):
    """Связь задания и задачи."""
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='assignment_tasks',
    )
    task = models.ForeignKey(
        'tasks.Task',
        on_delete=models.CASCADE,
        related_name='in_assignments',
    )
    order_number = models.PositiveIntegerField('Номер', default=0)

    class Meta:
        ordering = ['order_number']
        unique_together = ['assignment', 'task']


class GeneratedPDF(models.Model):
    """Сгенерированный PDF."""
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='pdfs',
    )
    variant_number = models.PositiveIntegerField('Номер варианта')
    file = models.FileField('PDF', upload_to='generated_pdfs/%Y/%m/')
    include_answers = models.BooleanField('С ответами', default=False)
    generated_at = models.DateTimeField('Дата', auto_now_add=True)

    class Meta:
        verbose_name = 'PDF'
        verbose_name_plural = 'PDF-файлы'
        ordering = ['variant_number']
