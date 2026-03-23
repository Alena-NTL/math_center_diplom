from django.core.management.base import BaseCommand
from tasks.models import Subject, Topic, DifficultyLevel, Task
from accounts.models import CustomUser


class Command(BaseCommand):
    help = 'Загружает примеры задач'

    def handle(self, *args, **options):
        # Берём преподавателя
        teacher = CustomUser.objects.filter(role='teacher').first()
        if not teacher:
            self.stdout.write(self.style.ERROR(
                'Сначала запустите: python manage.py load_initial_data'
            ))
            return

        easy = DifficultyLevel.objects.get(numeric_value=1)
        medium = DifficultyLevel.objects.get(numeric_value=2)
        hard = DifficultyLevel.objects.get(numeric_value=3)

        # === Квадратные уравнения (8 класс) ===
        topic_quad = Topic.objects.get(name='Квадратные уравнения')

        quad_tasks = [
            ('Решите уравнение $x^2 - 5x + 6 = 0$.', '$x = 2$ или $x = 3$', easy),
            ('Решите уравнение $x^2 + 4x - 12 = 0$.', '$x = 2$ или $x = -6$', easy),
            ('Решите уравнение $2x^2 - 7x + 3 = 0$.', '$x = 3$ или $x = 0{,}5$', medium),
            ('Решите уравнение $3x^2 + 5x - 2 = 0$.', '$x = \\frac{1}{3}$ или $x = -2$', medium),
            ('Решите уравнение $x^2 - 6x + 9 = 0$.', '$x = 3$', easy),
            ('Решите уравнение $x^2 + 2x + 1 = 0$.', '$x = -1$', easy),
            ('Решите уравнение $4x^2 - 4x + 1 = 0$.', '$x = 0{,}5$', medium),
            ('Решите уравнение $x^2 - 8x + 15 = 0$.', '$x = 3$ или $x = 5$', easy),
            ('Решите уравнение $x^2 + x - 30 = 0$.', '$x = 5$ или $x = -6$', easy),
            ('Решите уравнение $5x^2 - 3x - 2 = 0$.', '$x = 1$ или $x = -0{,}4$', medium),
            ('Найдите корни уравнения $x^2 = 49$.', '$x = 7$ или $x = -7$', easy),
            ('Решите уравнение $x^2 - 2x - 35 = 0$.', '$x = 7$ или $x = -5$', easy),
            ('При каких значениях $k$ уравнение $x^2 + kx + 4 = 0$ имеет два равных корня?',
             '$k = 4$ или $k = -4$', hard),
            ('Один из корней уравнения $x^2 + px - 18 = 0$ равен $3$. Найдите $p$ и второй корень.',
             '$p = 3$, второй корень $x = -6$', hard),
            ('Решите уравнение $x^2 - (2a+1)x + a^2 + a = 0$ при $a = 3$.',
             '$x = 3$ или $x = 4$', medium),
        ]

        count = 0
        for body, answer, diff in quad_tasks:
            _, created = Task.objects.get_or_create(
                body=body,
                defaults={
                    'author': teacher,
                    'topic': topic_quad,
                    'difficulty': diff,
                    'answer': answer,
                    'status': Task.Status.APPROVED,
                }
            )
            if created:
                count += 1

        # === Линейные уравнения (7 класс) ===
        topic_linear = Topic.objects.get(name='Линейные уравнения')

        linear_tasks = [
            ('Решите уравнение $3x + 7 = 22$.', '$x = 5$', easy),
            ('Решите уравнение $5x - 3 = 2x + 9$.', '$x = 4$', easy),
            ('Решите уравнение $2(x + 3) = 5x - 6$.', '$x = 4$', medium),
            ('Решите уравнение $\\frac{x}{3} + \\frac{x}{6} = 5$.', '$x = 10$', medium),
            ('Решите уравнение $7 - 4x = 3(1 - x)$.', '$x = 4$', easy),
            ('Решите уравнение $0{,}5x + 1{,}5 = 3{,}5$.', '$x = 4$', easy),
            ('Решите уравнение $\\frac{2x+1}{3} = \\frac{x-1}{2}$.', '$x = -5$', medium),
            ('Решите уравнение $4(x - 2) - 3(x + 1) = 5$.', '$x = 16$', medium),
            ('Решите уравнение $|2x - 6| = 10$.', '$x = 8$ или $x = -2$', hard),
            ('Решите уравнение $\\frac{3}{x-1} = 6$.', '$x = 1{,}5$', hard),
        ]

        for body, answer, diff in linear_tasks:
            _, created = Task.objects.get_or_create(
                body=body,
                defaults={
                    'author': teacher,
                    'topic': topic_linear,
                    'difficulty': diff,
                    'answer': answer,
                    'status': Task.Status.APPROVED,
                }
            )
            if created:
                count += 1

        # === Теорема Пифагора (8 класс) ===
        topic_pyth = Topic.objects.get(name='Теорема Пифагора')

        pyth_tasks = [
            ('Катеты прямоугольного треугольника равны $3$ и $4$. Найдите гипотенузу.',
             '$5$', easy),
            ('Гипотенуза прямоугольного треугольника равна $13$, один катет равен $5$. Найдите второй катет.',
             '$12$', easy),
            ('Катеты прямоугольного треугольника равны $6$ и $8$. Найдите гипотенузу.',
             '$10$', easy),
            ('Диагональ прямоугольника равна $10$, одна сторона равна $6$. Найдите вторую сторону.',
             '$8$', medium),
            ('Лестница длиной $5$ м приставлена к стене. Основание лестницы находится на расстоянии $3$ м от стены. На какой высоте лестница касается стены?',
             '$4$ м', medium),
            ('В прямоугольном треугольнике гипотенуза равна $\\sqrt{2}$, а один из катетов равен $1$. Найдите второй катет.',
             '$1$', medium),
            ('Найдите диагональ квадрата со стороной $5$.',
             '$5\\sqrt{2}$', medium),
            ('Стороны треугольника равны $5$, $12$ и $13$. Является ли он прямоугольным?',
             'Да, так как $5^2 + 12^2 = 13^2$', easy),
            ('В равнобедренном треугольнике боковая сторона равна $10$, а основание — $12$. Найдите высоту, проведённую к основанию.',
             '$8$', hard),
            ('Точка $M$ находится на расстоянии $3$ от точки $A(1, 1)$ и $4$ от точки $B(1, 5)$. Расстояние $AB = 5$. Найдите угол $AMB$.',
             '$90°$, так как $3^2 + 4^2 = 5^2$', hard),
        ]

        for body, answer, diff in pyth_tasks:
            _, created = Task.objects.get_or_create(
                body=body,
                defaults={
                    'author': teacher,
                    'topic': topic_pyth,
                    'difficulty': diff,
                    'answer': answer,
                    'status': Task.Status.APPROVED,
                }
            )
            if created:
                count += 1

        # === Площади фигур (8 класс) ===
        topic_area = Topic.objects.get(name='Площади фигур')

        area_tasks = [
            ('Найдите площадь прямоугольника со сторонами $7$ и $3$.', '$21$', easy),
            ('Найдите площадь квадрата со стороной $9$.', '$81$', easy),
            ('Найдите площадь треугольника с основанием $10$ и высотой $6$.',
             '$30$', easy),
            ('Найдите площадь параллелограмма с основанием $8$ и высотой $5$.',
             '$40$', easy),
            ('Найдите площадь трапеции с основаниями $6$ и $10$ и высотой $4$.',
             '$32$', medium),
            ('Найдите площадь ромба с диагоналями $6$ и $8$.',
             '$24$', medium),
            ('Стороны прямоугольника относятся как $3:4$, а периметр равен $28$. Найдите площадь.',
             '$48$', medium),
            ('Площадь прямоугольного треугольника равна $24$, один катет равен $6$. Найдите гипотенузу.',
             '$10$', hard),
        ]

        for body, answer, diff in area_tasks:
            _, created = Task.objects.get_or_create(
                body=body,
                defaults={
                    'author': teacher,
                    'topic': topic_area,
                    'difficulty': diff,
                    'answer': answer,
                    'status': Task.Status.APPROVED,
                }
            )
            if created:
                count += 1

        # === Вероятность (9 класс) ===
        topic_prob = Topic.objects.get(name='Классическая вероятность')

        prob_tasks = [
            ('В урне $3$ белых и $7$ чёрных шаров. Найдите вероятность вытащить белый шар.',
             '$0{,}3$', easy),
            ('Бросают два кубика. Найдите вероятность того, что сумма очков равна $7$.',
             '$\\frac{1}{6}$', medium),
            ('В классе $30$ учеников, из них $12$ девочек. Какова вероятность, что случайно выбранный ученик — девочка?',
             '$0{,}4$', easy),
            ('Монету бросают $3$ раза. Найдите вероятность выпадения ровно $2$ орлов.',
             '$\\frac{3}{8} = 0{,}375$', medium),
            ('Из колоды в $36$ карт наугад вытаскивают одну. Какова вероятность, что это туз?',
             '$\\frac{1}{9}$', easy),
            ('В коробке $5$ красных и $3$ синих карандаша. Наугад берут $2$. Какова вероятность, что оба красные?',
             '$\\frac{10}{28} = \\frac{5}{14}$', hard),
        ]

        for body, answer, diff in prob_tasks:
            _, created = Task.objects.get_or_create(
                body=body,
                defaults={
                    'author': teacher,
                    'topic': topic_prob,
                    'difficulty': diff,
                    'answer': answer,
                    'status': Task.Status.APPROVED,
                }
            )
            if created:
                count += 1

        self.stdout.write(self.style.SUCCESS(f'\nЗагружено {count} новых задач!'))
        total = Task.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Всего задач в базе: {total}'))
