from tasks.models import Task
from .models import ModerationLog


class ModerationService:

    @staticmethod
    def approve(task, moderator, comment=''):
        task.status = Task.Status.APPROVED
        task.save()
        ModerationLog.objects.create(
            task=task, moderator=moderator,
            action=ModerationLog.Action.APPROVED, comment=comment,
        )

    @staticmethod
    def reject(task, moderator, comment=''):
        task.status = Task.Status.REJECTED
        task.save()
        ModerationLog.objects.create(
            task=task, moderator=moderator,
            action=ModerationLog.Action.REJECTED, comment=comment,
        )

    @staticmethod
    def request_revision(task, moderator, comment):
        if not comment.strip():
            raise ValueError('Укажите, что нужно исправить')
        task.status = Task.Status.REVISION
        task.save()
        ModerationLog.objects.create(
            task=task, moderator=moderator,
            action=ModerationLog.Action.REVISION, comment=comment,
        )
