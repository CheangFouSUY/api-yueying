"""
This file contains all the utility functions for the entire program
"""

import sys
from io import BytesIO
from PIL import Image
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import BasePermission
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils import timezone
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

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

# Image compression, have quality and height, width is with respect to height
def get_thumbnail(f, quality, isThumbnail):
    try:
        maxWidthHeight = 256 if isThumbnail else 1024
        image = Image.open(f)
        baseWidth, baseHeight = image.size

        name = str(f).split('.')[0] + str(timezone.now())
        if isThumbnail:
            name += '-thumbnail'

        
        # don't resize if it's smaller than maxWidthHeight
        if baseWidth <= maxWidthHeight and baseHeight <= maxWidthHeight:
            finalWidth = baseWidth
            finalHeight = baseHeight
        elif baseWidth > baseHeight:
            aspectRatio = round(baseWidth / baseHeight)
            finalHeight = maxWidthHeight
            finalWidth = maxWidthHeight * aspectRatio
        else:
            aspectRatio = round(baseHeight / baseWidth)
            finalWidth = maxWidthHeight
            finalHeight = maxWidthHeight * aspectRatio

        thumbnail = BytesIO()

        # Resize/modify the image
        image = image.resize((finalWidth, finalHeight))

        # after modifications, save it to the thumbnail
        image.save(thumbnail, format='JPEG', quality=quality)
        thumbnail.seek(0)

        newImage = InMemoryUploadedFile(thumbnail, 'ImageField', "%s.jpg" % name, 'image/jpeg',
                                        sys.getsizeof(thumbnail), None)
        return newImage
    except Exception as e:
        return e