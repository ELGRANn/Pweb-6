from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
import smtplib  
from django.conf import settings


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
    from django.core.mail import send_mail
from django.conf import settings

def enviar_correo(request):
    if request.method == 'POST':
        destinatario = request.POST.get('destinatario')
        asunto = request.POST.get('asunto')
        contenido = request.POST.get('contenido')

        from_email = settings.EMAIL_HOST_USER
        recipient_list = [destinatario]

        try:
            message_html = render_to_string('pdfapp/plantilla_mail.html', {'titulo': asunto, 'contenido': contenido})

            email = EmailMessage(
                subject=asunto,
                body=message_html,
                from_email=from_email,
                to=recipient_list
            )
            email.content_subtype = 'html'  
            email.send()

            return HttpResponse("Correo enviado exitosamente")
        except Exception as e:
            return HttpResponse(f"Error al enviar el correo: {str(e)}", status=500)

    return render(request, 'pdfapp/formulario_correo.html')