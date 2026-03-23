from django.db import models
from django.conf import settings


class ModerationLog(models.Model):
    """Журнал модерации."""

    class Action(models.TextChoices):
        SUBMITTED = 'submitted', 'Отправлена на модерацию'
        APPROVED = 'approved', 'Одобрена'
        REJECTED = 'rejected', 'Отклонена'
        REVISION = 'revision', 'Возвращена на доработку'

    task = models.ForeignKey(
        'tasks.Task',
        on_delete=models.CASCADE,
        related_name='moderation_logs',
        verbose_name='Задачу',
    )
    moderator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='moderation_actions',
        verbose_name='Модератор',
    )
    action = models.CharField('Действие', max_length=15, choices=Action.choices)
    comment = models.TextField('Комментарий', blank=True)
    created_at = models.DateTimeField('Дата', auto_now_add=True)

    class Meta:
        verbose_name = 'Запись модерации'
        verbose_name_plural = 'Журнал модерации'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.get_action_display()} — Задача #{self.task.pk}'
