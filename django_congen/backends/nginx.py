from django_congen.backends.generic import GenericHandler


class NginxHandler(GenericHandler):
    template = 'django_congen/nginx'

