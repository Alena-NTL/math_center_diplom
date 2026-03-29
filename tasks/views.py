from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from accounts.decorators import teacher_required
from .models import Task, TaskImage
from .forms import TaskForm, TaskFilterForm


@login_required
def task_list_view(request):
    """Список задач с фильтрами."""
    form = TaskFilterForm(request.GET)
    tasks = Task.objects.select_related('topic', 'topic__subject', 'difficulty', 'author')

    if form.is_valid():
        if form.cleaned_data.get('search'):
            q = form.cleaned_data['search']
            tasks = tasks.filter(Q(body__icontains=q) | Q(answer__icontains=q))

        if form.cleaned_data.get('subject'):
            tasks = tasks.filter(topic__subject_id=form.cleaned_data['subject'])

        if form.cleaned_data.get('grade'):
            tasks = tasks.filter(topic__grade=form.cleaned_data['grade'])

        if form.cleaned_data.get('difficulty'):
            tasks = tasks.filter(difficulty_id=form.cleaned_data['difficulty'])

        if form.cleaned_data.get('status'):
            tasks = tasks.filter(status=form.cleaned_data['status'])

    # Преподаватель видит свои + одобренные
    if request.user.is_teacher:
        tasks = tasks.filter(
            Q(author=request.user) | Q(status=Task.Status.APPROVED)
        )

    paginator = Paginator(tasks, 20)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'tasks/task_list.html', {
        'tasks': page,
        'filter_form': form,
    })


@login_required
def task_detail_view(request, pk):
    """Просмотр задачи."""
    task = get_object_or_404(
        Task.objects.select_related('topic', 'topic__subject', 'difficulty', 'author'),
        pk=pk,
    )
    images = task.images.all()
    logs = task.moderation_logs.select_related('moderator').all()

    return render(request, 'tasks/task_detail.html', {
        'task': task,
        'images': images,
        'logs': logs,
    })


@teacher_required
def task_create_view(request):
    """Создание задачи."""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.status = Task.Status.DRAFT
            task.save()

            # Сохраняем изображения
            for f in request.FILES.getlist('images'):
                TaskImage.objects.create(task=task, image=f)

            messages.success(request, 'Задача создана как черновик!')
            return redirect('tasks:detail', pk=task.pk)
    else:
        form = TaskForm()

    return render(request, 'tasks/task_create.html', {'form': form})


@teacher_required
def task_edit_view(request, pk):
    """Редактирование задачи."""
    task = get_object_or_404(Task, pk=pk)

    # Только автор или админ
    if task.author != request.user and not request.user.is_admin_role:
        messages.error(request, 'Вы можете редактировать только свои задачи')
        return redirect('tasks:detail', pk=pk)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задача обновлена!')
            return redirect('tasks:detail', pk=pk)
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/task_edit.html', {'form': form, 'task': task})


@teacher_required
def task_submit_view(request, pk):
    """Отправить на модерацию."""
    task = get_object_or_404(Task, pk=pk, author=request.user)

    if task.status in (Task.Status.DRAFT, Task.Status.REVISION, Task.Status.REJECTED):
        task.status = Task.Status.ON_REVIEW
        task.save()

        # Записываем в лог модерации
        from moderation.models import ModerationLog
        ModerationLog.objects.create(
            task=task,
            moderator=request.user,
            action=ModerationLog.Action.SUBMITTED,
        )

        messages.success(request, 'Задача отправлена на модерацию!')
    else:
        messages.error(request, 'Невозможно отправить эту задачу на модерацию')

    return redirect('tasks:detail', pk=pk)

