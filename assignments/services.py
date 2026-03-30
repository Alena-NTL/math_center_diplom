import random
from math import comb


class InsufficientTasksError(Exception):
    pass


class AssignmentService:

    @staticmethod
    def get_available_tasks(subject=None, grade=None, difficulty=None):
        from tasks.models import Task
        qs = Task.objects.filter(status=Task.Status.APPROVED)
        if subject:
            qs = qs.filter(topic__subject=subject)
        if grade:
            qs = qs.filter(topic__grade=grade)
        if difficulty:
            qs = qs.filter(difficulty=difficulty)
        return qs.select_related('topic', 'difficulty')

    @staticmethod
    def generate_unique_variants(task_pool, tasks_per_variant, num_variants):
        task_list = list(task_pool)

        if len(task_list) < tasks_per_variant:
            raise InsufficientTasksError(
                f'Нужно минимум {tasks_per_variant} задач, '
                f'доступно {len(task_list)}. '
                f'Добавьте задач или уменьшите количество.'
            )

        max_combos = comb(len(task_list), tasks_per_variant)
        if max_combos < num_variants:
            raise InsufficientTasksError(
                f'Из {len(task_list)} задач можно составить максимум '
                f'{max_combos} уникальных вариантов. Запрошено: {num_variants}.'
            )

        selected = set()
        while len(selected) < num_variants:
            combo = tuple(sorted(
                random.sample(task_list, tasks_per_variant),
                key=lambda t: t.pk,
            ))
            selected.add(combo)

        variants = []
        for combo in selected:
            v = list(combo)
            random.shuffle(v)
            variants.append(v)

        return variants
