from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
import smtplib  


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
    subject = "Asunto con ñ"
    context = {
        'titulo': "Este es el título del correo",
        'contenido': "Este es el cuerpo del mensaje con ñ y otros caracteres especiales."
    }
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['destinatario@example.com']

    try:
        message_html = render_to_string('pdfapp/plantilla_mail.html', context)

        email = EmailMessage(
            subject=subject,
            body=message_html,
            from_email=from_email,
            to=recipient_list
        )
        email.content_subtype = 'html'  # Indica que el cuerpo del mensaje está en formato HTML
        email.encoding = 'utf-8'  # Establecer la codificación a UTF-8
        email.send()
        return HttpResponse("Correo enviado exitosamente")
    except smtplib.SMTPException as e:
        return HttpResponse(f"Error al enviar el correo: {str(e)}", status=500)