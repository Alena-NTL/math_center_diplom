from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import FileResponse

from accounts.decorators import teacher_required
from tasks.models import Task
from .models import Assignment, AssignmentTask, GeneratedPDF
from .forms import AutoGenerateForm
from .services import AssignmentService, InsufficientTasksError
from pdf_generator.services import PDFGeneratorService


@teacher_required
def assignment_list_view(request):
    assignments = Assignment.objects.filter(
        created_by=request.user
    ).prefetch_related('pdfs')
    return render(request, 'assignments/list.html', {'assignments': assignments})


@teacher_required
def assignment_create_view(request):
    approved_count = Task.objects.filter(status=Task.Status.APPROVED).count()

    if request.method == 'POST':
        form = AutoGenerateForm(request.POST)
        if form.is_valid():
            try:
                # 1. Получаем задачи
                pool = AssignmentService.get_available_tasks(
                    subject=form.cleaned_data['subject'],
                    grade=form.cleaned_data['grade'],
                    difficulty=form.cleaned_data.get('difficulty'),
                )

                # 2. Генерируем варианты
                variants = AssignmentService.generate_unique_variants(
                    task_pool=pool,
                    tasks_per_variant=form.cleaned_data['tasks_per_variant'],
                    num_variants=form.cleaned_data['num_variants'],
                )

                # 3. Создаём Assignment
                subj = form.cleaned_data['subject']
                grade = form.cleaned_data['grade']
                assignment = Assignment.objects.create(
                    created_by=request.user,
                    title=f'{subj}, {grade} класс',
                    grade=grade,
                )

                # 4. Генерируем PDF
                pdf_service = PDFGeneratorService()
                include_answers = form.cleaned_data.get('include_answers', False)

                for i, variant_tasks in enumerate(variants, 1):
                    # Сохраняем задачи первого варианта
                    if i == 1:
                        for j, task in enumerate(variant_tasks, 1):
                            AssignmentTask.objects.create(
                                assignment=assignment, task=task, order_number=j,
                            )

                    pdf_path = pdf_service.generate(
                        assignment=assignment,
                        tasks=variant_tasks,
                        variant_number=i,
                        include_answers=include_answers,
                    )
                    GeneratedPDF.objects.create(
                        assignment=assignment,
                        variant_number=i,
                        file=pdf_path,
                        include_answers=include_answers,
                    )

                messages.success(request, f'Создано {len(variants)} вариантов!')
                return redirect('assignments:detail', pk=assignment.pk)

            except InsufficientTasksError as e:
                messages.error(request, str(e))
    else:
        form = AutoGenerateForm()

    return render(request, 'assignments/create.html', {
        'form': form,
        'approved_count': approved_count,
    })


@teacher_required
def assignment_detail_view(request, pk):
    assignment = get_object_or_404(
        Assignment.objects.prefetch_related('assignment_tasks__task', 'pdfs'),
        pk=pk, created_by=request.user,
    )
    return render(request, 'assignments/detail.html', {'assignment': assignment})


@teacher_required
def download_pdf_view(request, pk):
    pdf = get_object_or_404(GeneratedPDF, pk=pk)
    return FileResponse(
        open(pdf.file.path, 'rb'),
        content_type='application/pdf',
        as_attachment=True,
        filename=f'variant_{pdf.variant_number}.pdf',
    )
