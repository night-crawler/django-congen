from django_congen.backends.generic import GenericHandler


class SupervisordHandler(GenericHandler):
    template = 'django_congen/supervisord'
