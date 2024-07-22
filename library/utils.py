from email.utils import make_msgid
from django.core.mail import EmailMessage
from django.conf import settings
import uuid

def send_email(title, html_content, recipient_address, cc_address = [], reply_to_address=None):
    try:
        message_id = make_msgid(idstring=str(uuid.uuid4()))
        headers = {
            'Message-ID': message_id,
            'References': message_id,
            'In-Reply-To': message_id,
            }
        if reply_to_address != None:
            headers['Reply-To'] = reply_to_address

        if len(cc_address):
            email = EmailMessage(subject=title, body=html_content, from_email=settings.EMAIL_HOST_USER, to=[recipient_address], headers=headers, cc=cc_address)
        else:
            email = EmailMessage(subject=title, body=html_content, from_email=settings.EMAIL_HOST_USER, to=[recipient_address], headers=headers)
        email.content_subtype = 'html'
        email.send()    
        return True
    except Exception as e:
        print('Email sending Error: ', str(e))
        return False