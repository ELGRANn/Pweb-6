from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.mail import send_mail


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def generate_invoice(request):
    context = {
        'date': '2024-06-24',
        'company_name': 'My Company',
        'company_address': '1234 Street, City, Country',
        'client_name': 'John Doe',
        'client_address': '5678 Avenue, City, Country',
        'items': [
            {'name': 'Item 1', 'price': '$10.00'},
            {'name': 'Item 2', 'price': '$20.00'},
            {'name': 'Item 3', 'price': '$30.00'},
        ],
        'total': '$60.00'
    }
    return render_to_pdf('pdfapp/invoice.html', context)

def enviar_correo(request):
    asunto = 'asunto del correo'
    mensaje = 'mensaje del correo'
    email = 'tu_email@gmail.com'
    listaContendora = ['destinatario1@gmail.com', 'destinatario2@gmail.com']
    
    send_mail(asunto,mensaje, email,  listaContendora)
    
    return HttpResponse("Correo enviado exitosamente")
