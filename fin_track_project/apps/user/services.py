from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string, select_template
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tokens import email_verification_token


def send_verification_email(request, user):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_verification_token.make_token(user)
    verification_url = request.build_absolute_uri(
        reverse(
            'user:verify_email',
            kwargs={'uidb64': uidb64, 'token': token},
        )
    )

    context = {
        'user': user,
        'verification_url': verification_url,
    }

    subject = 'Confirme seu cadastro no FinTrack'
    text_template = select_template(
        [
            'apps/user/email_verification_email.txt',
            'apps/user/email_verification_email_context.txt',
        ]
    )
    text_content = text_template.render(context)
    html_content = render_to_string(
        'apps/user/email_verification_email.html',
        context,
    )

    message = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    message.attach_alternative(html_content, 'text/html')
    message.send(fail_silently=False)
