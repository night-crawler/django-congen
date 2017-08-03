from django.conf import settings

MAX_DEPTH = getattr(settings, 'CONGEN_MAX_DEPTH', 3)
PATH_BUILDER = 'django_congen.util:PathBuilder'
