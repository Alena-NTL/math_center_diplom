from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tasks.models import Task
from assignments.models import Assignment


@login_required
def index_view(request):
    ctx = {
        'total_approved': Task.objects.filter(status=Task.Status.APPROVED).count(),
        'on_review': Task.objects.filter(status=Task.Status.ON_REVIEW).count(),
        'my_tasks': Task.objects.filter(author=request.user).count(),
        'my_assignments': Assignment.objects.filter(created_by=request.user).count(),
        'my_recent': Task.objects.filter(author=request.user).select_related('topic')[:5],
    }
    return render(request, 'dashboard/index.html', ctx)

