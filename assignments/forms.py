from django import forms
from tasks.models import Subject, DifficultyLevel


class AutoGenerateForm(forms.Form):
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        label='Предмет',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    grade = forms.ChoiceField(
        choices=[(i, f'{i} класс') for i in range(5, 12)],
        label='Класс',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    difficulty = forms.ModelChoiceField(
        queryset=DifficultyLevel.objects.all(),
        label='Сложность',
        required=False,
        empty_label='Любая',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    tasks_per_variant = forms.IntegerField(
        label='Задач в варианте',
        min_value=1, max_value=20, initial=5,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )
    num_variants = forms.IntegerField(
        label='Количество вариантов',
        min_value=1, max_value=30, initial=4,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )
    include_answers = forms.BooleanField(
        label='Включить ответы в PDF',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
