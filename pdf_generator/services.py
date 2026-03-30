import os
import re
from io import BytesIO
from datetime import datetime

from django.conf import settings

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class PDFGeneratorService:

    def __init__(self):
        self._register_fonts()
        self._create_styles()

    def _register_fonts(self):
        font_dir = os.path.join(settings.BASE_DIR, 'static', 'fonts')
        try:
            pdfmetrics.registerFont(TTFont('DejaVu', os.path.join(font_dir, 'DejaVuSans.ttf')))
            pdfmetrics.registerFont(TTFont('DejaVu-Bold', os.path.join(font_dir, 'DejaVuSans-Bold.ttf')))
            self.font = 'DejaVu'
            self.font_bold = 'DejaVu-Bold'
        except Exception:
            self.font = 'Helvetica'
            self.font_bold = 'Helvetica-Bold'

    def _create_styles(self):
        self.style_title = ParagraphStyle(
            'Title', fontName=self.font_bold, fontSize=16,
            alignment=TA_CENTER, spaceAfter=6 * mm,
        )
        self.style_subtitle = ParagraphStyle(
            'Subtitle', fontName=self.font, fontSize=11,
            alignment=TA_CENTER, spaceAfter=8 * mm, textColor='#666666',
        )
        self.style_task_num = ParagraphStyle(
            'TaskNum', fontName=self.font_bold, fontSize=11,
            spaceAfter=2 * mm,
        )
        self.style_task_body = ParagraphStyle(
            'TaskBody', fontName=self.font, fontSize=11,
            leading=16, spaceAfter=4 * mm,
        )
        self.style_answer = ParagraphStyle(
            'Answer', fontName=self.font, fontSize=10,
            leading=14, textColor='#444444',
        )

    def _render_latex(self, latex_str):
        """Рендерит LaTeX в PNG."""
        fig, ax = plt.subplots(figsize=(0.01, 0.01))
        ax.axis('off')
        ax.text(0, 0, f'${latex_str}$', fontsize=14, transform=ax.transAxes)
        buf = BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', dpi=150,
                    pad_inches=0.05, facecolor='white')
        plt.close(fig)
        buf.seek(0)
        return buf

    def _text_to_elements(self, text, style):
        """Разбивает текст на части: обычный текст и LaTeX-формулы."""
        elements = []
        parts = re.split(r'(\$[^$]+\$)', text)
        current = ''

        for part in parts:
            if part.startswith('$') and part.endswith('$') and len(part) > 2:
                # Сначала добавляем накопленный текст
                if current.strip():
                    safe = current.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    elements.append(Paragraph(safe, style))
                    current = ''

                # Рендерим формулу
                try:
                    latex = part[1:-1]
                    img_buf = self._render_latex(latex)
                    img = RLImage(img_buf)
                    # Ограничиваем размер
                    max_w = 14 * cm
                    if img.drawWidth > max_w:
                        ratio = max_w / img.drawWidth
                        img.drawWidth = max_w
                        img.drawHeight *= ratio
                    elements.append(img)
                except Exception:
                    current += part
            else:
                current += part

        if current.strip():
            safe = current.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            elements.append(Paragraph(safe, style))

        return elements

    def generate(self, assignment, tasks, variant_number, include_answers=False):
        """
        Генерирует PDF для одного варианта.
        Возвращает относительный путь к файлу.
        """
        # Папка
        date_dir = datetime.now().strftime('%Y/%m')
        pdf_dir = os.path.join(settings.MEDIA_ROOT, 'generated_pdfs', date_dir)
        os.makedirs(pdf_dir, exist_ok=True)

        filename = f'assignment_{assignment.pk}_v{variant_number}.pdf'
        filepath = os.path.join(pdf_dir, filename)
        relative = os.path.join('generated_pdfs', date_dir, filename)

        doc = SimpleDocTemplate(
            filepath, pagesize=A4,
            leftMargin=2 * cm, rightMargin=2 * cm,
            topMargin=2 * cm, bottomMargin=2 * cm,
        )

        elements = []

        # Шапка
        elements.append(Paragraph(assignment.title, self.style_title))
        elements.append(Paragraph(
            f'Вариант {variant_number} &nbsp;&nbsp;|&nbsp;&nbsp; '
            f'{datetime.now().strftime("%d.%m.%Y")}',
            self.style_subtitle,
        ))
        elements.append(Spacer(1, 3 * mm))

        # Задачи
        for i, task in enumerate(tasks, 1):
            elements.append(Paragraph(f'Задача {i}.', self.style_task_num))
            task_elements = self._text_to_elements(task.body, self.style_task_body)
            elements.extend(task_elements)
            elements.append(Spacer(1, 3 * mm))

        # Ответы
        if include_answers:
            elements.append(Spacer(1, 8 * mm))
            elements.append(Paragraph('Ответы:', self.style_task_num))
            for i, task in enumerate(tasks, 1):
                answer_elements = self._text_to_elements(
                    f'{i}) {task.answer}', self.style_answer
                )
                elements.extend(answer_elements)

        doc.build(elements)
        return relative
