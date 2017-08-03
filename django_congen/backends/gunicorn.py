from django_congen.backends.generic import GenericHandler


class GunicornHandler(GenericHandler):
    template = 'django_congen/gunicorn_release.py'
