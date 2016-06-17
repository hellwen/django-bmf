#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.conf import settings

import jwt


def decode_handler(token):
    return jwt.decode(
        token,
        settings.AUTH_SECRET_KEY,
        audience=settings.AUTH_AUDIENCE,
        issuer=settings.AUTH_ISSUER,
        algorithms=settings.AUTH_ALGORITHMS,
    )
