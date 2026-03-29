from django import forms
from .models import Task, Topic


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['topic', 'difficulty', 'body', 'answer', 'solution']
        widgets = {
            'topic': forms.Select(attrs={'class': 'form-select'}),
            'difficulty': forms.Select(attrs={'class': 'form-select'}),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Текст задачи. Для формул: $x^2 + 3x = 0$',
            }),
            'answer': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Ответ',
            }),
            'solution': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Решение (необязательно)',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['topic'].queryset = Topic.objects.select_related(
            'subject'
        ).order_by('subject__name', 'grade', 'name')


class TaskFilterForm(forms.Form):
    """Фильтры для поиска задач."""

    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по тексту...',
        }),
    )
    subject = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    grade = forms.ChoiceField(
        required=False,
        choices=[('', 'Все классы')] + [(i, f'{i} класс') for i in range(5, 12)],
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    difficulty = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'Все статусы')] + list(Task.Status.choices),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        from .models import Subject, DifficultyLevel

        # Заполняем выбор предметов
        subjects = [('', 'Все предметы')]
        subjects += [(s.pk, s.name) for s in Subject.objects.all()]
        self.fields['subject'].choices = subjects

        # Заполняем выбор сложности
        diffs = [('', 'Любая сложность')]
        diffs += [(d.pk, d.name) for d in DifficultyLevel.objects.all()]
        self.fields['difficulty'].choices = diffs
