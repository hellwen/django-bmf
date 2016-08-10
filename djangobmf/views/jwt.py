#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _

from djangobmf.authentication import JWTAuthentication
from djangobmf.utils.jwt import payload_handler
from djangobmf.utils.jwt import encode_handler
from djangobmf.utils.jwt import payload_update

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView


class JSONWebTokenAPIView(APIView):
    """
    """
    permission_classes = ()
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        """
        Verify JWT
        """
        try:
            auth = JWTAuthentication().authenticate(request)
        except AuthenticationFailed:
            return Response({'token': None}, status=HTTP_401_UNAUTHORIZED)
        if not auth:
            return Response({'token': None}, status=HTTP_401_UNAUTHORIZED)
        return Response({'token': auth[1]})

    def post(self, request, *args, **kwargs):
        """
        Generate JWT
        """
        credentials = dict(request.data.items())
        credentials['request'] = request
        user = authenticate(**credentials)

        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                return Response({'error': msg}, status=HTTP_401_UNAUTHORIZED)
            return Response({'token': encode_handler(payload_handler(user))})

        msg = _('Unable to login with provided credentials.')
        return Response({'error': msg}, status=HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        """
        Refresh JWT
        """
        try:
            auth = JWTAuthentication().authenticate(request, payload=True)
        except AuthenticationFailed:
            return Response({'token': None}, status=HTTP_401_UNAUTHORIZED)
        if not auth:
            return Response({'token': None}, status=HTTP_401_UNAUTHORIZED)

        if not auth[0].is_active:
            msg = _('User account is disabled.')
            return Response({'error': msg}, status=HTTP_401_UNAUTHORIZED)

        return Response({'token': encode_handler(payload_update(auth[1]))})
