from django.core.management.base import BaseCommand
from tasks.models import Subject, Topic, DifficultyLevel
from accounts.models import CustomUser


class Command(BaseCommand):
    help = 'Загружает начальные данные'

    def handle(self, *args, **options):

        # === Уровни сложности ===
        difficulties = [
            ('Базовый', 1),
            ('Средний', 2),
            ('Сложный', 3),
            ('Олимпиадный', 4),
        ]
        for name, value in difficulties:
            obj, created = DifficultyLevel.objects.get_or_create(
                name=name, defaults={'numeric_value': value}
            )
            if created:
                self.stdout.write(f'  + Сложность: {name}')

        # === Предметы ===
        algebra, _ = Subject.objects.get_or_create(
            name='Алгебра', defaults={'sort_order': 1}
        )
        geometry, _ = Subject.objects.get_or_create(
            name='Геометрия', defaults={'sort_order': 2}
        )
        probability, _ = Subject.objects.get_or_create(
            name='Теория вероятностей', defaults={'sort_order': 3}
        )

        # === Темы: Алгебра ===
        algebra_topics = [
            ('Линейные уравнения', 7),
            ('Системы линейных уравнений', 7),
            ('Квадратные уравнения', 8),
            ('Теорема Виета', 8),
            ('Системы уравнений', 9),
            ('Неравенства', 9),
            ('Функции и графики', 9),
            ('Арифметическая прогрессия', 9),
            ('Геометрическая прогрессия', 9),
            ('Степени и корни', 8),
            ('Логарифмы', 10),
            ('Тригонометрия', 10),
            ('Производная', 11),
            ('Интегралы', 11),
        ]
        for i, (name, grade) in enumerate(algebra_topics):
            Topic.objects.get_or_create(
                name=name, subject=algebra,
                defaults={'grade': grade, 'sort_order': i}
            )

        # === Темы: Геометрия ===
        geometry_topics = [
            ('Треугольники', 7),
            ('Признаки равенства треугольников', 7),
            ('Четырёхугольники', 8),
            ('Теорема Пифагора', 8),
            ('Окружность', 8),
            ('Площади фигур', 8),
            ('Подобие треугольников', 9),
            ('Векторы', 9),
            ('Координатный метод', 9),
            ('Стереометрия: начало', 10),
            ('Многогранники', 11),
        ]
        for i, (name, grade) in enumerate(geometry_topics):
            Topic.objects.get_or_create(
                name=name, subject=geometry,
                defaults={'grade': grade, 'sort_order': i}
            )

        # === Темы: Теория вероятностей ===
        prob_topics = [
            ('Классическая вероятность', 9),
            ('Комбинаторика', 9),
            ('Статистика', 8),
        ]
        for i, (name, grade) in enumerate(prob_topics):
            Topic.objects.get_or_create(
                name=name, subject=probability,
                defaults={'grade': grade, 'sort_order': i}
            )

        self.stdout.write(self.style.SUCCESS('Справочники загружены!'))

        # === Тестовый преподаватель ===
        if not CustomUser.objects.filter(username='teacher1').exists():
            CustomUser.objects.create_user(
                username='teacher1',
                password='teacher123',
                first_name='Алёна',
                last_name='Пудова',
                patronymic='Алексеевна',
                role='teacher',
            )
            self.stdout.write(self.style.SUCCESS('Создан преподаватель: teacher1 / teacher123'))

        # === Устанавливаем роль admin для суперпользователя ===
        for user in CustomUser.objects.filter(is_superuser=True):
            if user.role != 'admin':
                user.role = 'admin'
                user.save()
                self.stdout.write(f'  Роль admin установлена для {user.username}')

        self.stdout.write(self.style.SUCCESS('\nГотово! Можно работать.'))
