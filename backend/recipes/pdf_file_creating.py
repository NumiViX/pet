from datetime import datetime
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from backend.variables import (FONT_SIZE_12, INDENTATION_VALUE_20,
                               INDENTATION_VALUE_100, INDENTATION_VALUE_800,
                               MIN_NUM_0)


def create_pdf_file(shopping_cart):
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'recipes/ttf/DejaVuSans.ttf'))
    now = datetime.now()
    timestamp = now.strftime('%Y_%m_%d')
    buffer = BytesIO()
    pdf_file = canvas.Canvas(buffer, pagesize=A4)

    pdf_file.setFont('DejaVuSans', FONT_SIZE_12)
    pdf_file.drawString(INDENTATION_VALUE_100,
                        INDENTATION_VALUE_800,
                        f'Список покупок на {timestamp}:')
    indentation_value = INDENTATION_VALUE_800 - INDENTATION_VALUE_20
    for ingredient in shopping_cart:
        pdf_file.drawString(
            INDENTATION_VALUE_100,
            indentation_value,
            f'{ingredient.get("ingredients__name")} '
            f'{ingredient.get("amount")} '
            f'{ingredient.get("ingredients__measurement_unit")}'
        )
        indentation_value -= INDENTATION_VALUE_20
    pdf_file.showPage()
    pdf_file.save()
    buffer.seek(MIN_NUM_0)
    return buffer
