from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.decorators import admin_required
from tasks.models import Task
from .services import ModerationService


@admin_required
def moderation_queue_view(request):
    tasks = Task.objects.filter(
        status=Task.Status.ON_REVIEW
    ).select_related('topic', 'difficulty', 'author').order_by('created_at')

    return render(request, 'moderation/queue.html', {'tasks': tasks})


@admin_required
def moderation_review_view(request, pk):
    task = get_object_or_404(Task, pk=pk, status=Task.Status.ON_REVIEW)
    logs = task.moderation_logs.select_related('moderator').all()

    if request.method == 'POST':
        action = request.POST.get('action')
        comment = request.POST.get('comment', '')

        try:
            if action == 'approve':
                ModerationService.approve(task, request.user, comment)
                messages.success(request, f'Задача #{task.pk} одобрена!')
            elif action == 'reject':
                ModerationService.reject(task, request.user, comment)
                messages.info(request, f'Задача #{task.pk} отклонена')
            elif action == 'revision':
                ModerationService.request_revision(task, request.user, comment)
                messages.info(request, f'Задача #{task.pk} возвращена на доработку')
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('moderation:review', pk=pk)

        return redirect('moderation:queue')

    return render(request, 'moderation/review.html', {'task': task, 'logs': logs})
