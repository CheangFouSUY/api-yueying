"""
This file contains all the utility functions for the entire program
"""

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import BasePermission


def get_tokens(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }