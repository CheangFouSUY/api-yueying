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
import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
import requests


def get_tokens(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def send_smtp(user, request, token, subject, fileName, isActivate):
    #domain = settings.BACKEND_URL if isActivate else settings.FRONTEND_URL
    domain = settings.FRONTEND_URL
    context = {
        'request': request,
        'protocol': request.scheme,

        # for unit tests:
        # 'domain': "no_domain_name",

        # for production
        'domain': domain,
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
def get_thumbnail(f, quality, isThumbnail, ratio):
    try:
        maxWidthHeight = 256 if isThumbnail else 1024
        image = Image.open(f)
        baseWidth, baseHeight = image.size

        name = str(f).split('.')[0] + str(timezone.now())
        if isThumbnail:
            name += '-thumbnail'

        if ratio != 0: # incase ratio is not defined
            finalHeight = maxWidthHeight
            finalWidth = int (maxWidthHeight * ratio)
        # don't resize if it's smaller than maxWidthHeight
        elif baseWidth <= maxWidthHeight and baseHeight <= maxWidthHeight:
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
        # image.save(thumbnail, format='JPEG', quality=quality)
        image.save(thumbnail, format='PNG', quality=quality)
        thumbnail.seek(0)

        newImage = InMemoryUploadedFile(thumbnail, 'ImageField', "%s.jpg" % name, 'image/jpeg',
                                        sys.getsizeof(thumbnail), None)
        return newImage
    except Exception as e:
        return e


def generate_presigned_url(object_key, expiry=3600):

    client = boto3.client("s3",region_name=settings.AWS_S3_REGION_NAME,
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    try:
        response = client.generate_presigned_url('get_object',
                                                  Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME,'Key': object_key},
                                                  ExpiresIn=expiry)
        return(response)
    except ClientError as e:
        return(e)