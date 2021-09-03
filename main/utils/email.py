from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class Email:
    from_email = 'ANTORUS.COM – Your boosting store <shop@antorus.com>'

    def send_order(self, order, template):
        subject = 'Order №' + order.get_order_number()
        html_message = render_to_string(template, {'order': order})
        plain_message = strip_tags(html_message)
        to = order.email.lower()
        msg = EmailMultiAlternatives(subject, html_message, 'shop@antorus.com', [to],
                                     bcc=['antorus.com+2860455185@invite.trustpilot.com'])
        msg.content_subtype = "html"
        msg.send()
        if order.status == '1':
            mail.send_mail(subject, plain_message, self.from_email, ['antorusshop@gmail.com'],
                           html_message=html_message)

    def send_new_password(self, user, password):
        subject = 'Antorus - reset password'
        to = user.email.lower()
        message = f'Your new password: {password}'
        html_message = render_to_string('email/registration.html', {'message': message, 'user': user.username})
        plain_message = strip_tags(html_message)
        mail.send_mail(subject, plain_message, self.from_email, [to], html_message=html_message)

    def create_account(self, email, url, username):
        subject = 'Antorus - registration'
        to = email.lower()
        message = 'To activate your account click on the link:'
        html_message = render_to_string('email/registration.html',
                                        {'message': message, 'link': url, 'user': username})
        plain_message = strip_tags(html_message)
        mail.send_mail(subject, plain_message, self.from_email, [to], html_message=html_message)
