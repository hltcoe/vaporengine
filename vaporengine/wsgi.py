"""
WSGI config for vaporengine project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import sys

# Activate the virtual environment, if it exists.
# This code was tested with Apache 2.2 on Debian 7
VIRTUALENV_PATH=os.path.join(os.path.dirname(__file__), "../venv/")
if os.path.isdir(VIRTUALENV_PATH):
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    activate_env=os.path.join(VIRTUALENV_PATH, "bin/activate_this.py")
    execfile(activate_env, dict(__file__=activate_env))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vaporengine.settings")

application = get_wsgi_application()
