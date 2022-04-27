"""
This file contains all the utility functions for the entire program
"""

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import BasePermission
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


def get_tokens(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def send_smtp(user, request, token, subject, fileName):
    context = {
        'request': request,
        'protocol': request.scheme,

        # 
        'domain': settings.BACKEND_URL,
        'username': user.username,
        'token': str(token),
        'email': user.email
    }

    email = EmailMessage(
        subject,
        render_to_string(fileName, context),
        settings.EMAIL_FROM_USER, # FROM
        [user.email],    #TO
    )

    email.send(fail_silently=False)