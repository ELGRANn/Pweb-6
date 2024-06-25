from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML

def generate_pdf(request):
    template = get_template('pdfapp/sample_template.html')
    context = {
        'title': 'Rendirizador de PDF',
        'content': 'PDF generado desde HTML',
    }
    html_content = template.render(context)
    pdf_file = HTML(string=html_content).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="sample.pdf"'
    return response
