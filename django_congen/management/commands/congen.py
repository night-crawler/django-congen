import typing as t

from django.core.management.base import BaseCommand
from importlib import import_module

from django.template import TemplateDoesNotExist

from django_congen.settings import MAX_DEPTH, PATH_BUILDER
from django_congen.backends.generic import GenericHandler
from django_congen.util import PathBuilder

"""
tree:
virtualenv
├── bin
├── project
│   ├── congen
│   │   ├── management
│   ├── project
│   ├── manage.py
"""


class Command(BaseCommand):
    help = ('Generates various configs. Example:\n'
            'python manage.py congen supervisord')

    requires_model_validation = False

    def add_arguments(self, parser):
        parser.add_argument('--backend', '-b', default=0, dest='backend', help='set backend')
        parser.add_argument('--print', '-p', action='store_true', default=False, dest='print',
                            help='print collected variables', )

    @staticmethod
    def get_path_builder() -> t.Type[PathBuilder]:
        _pb_mod, _pb_class = PATH_BUILDER.split(':')
        pb_mod = import_module(_pb_mod)
        return getattr(pb_mod, _pb_class)

    @staticmethod
    def get_handler(backend_name) -> t.Type[GenericHandler]:
        mod = import_module('django_congen.backends.%s' % backend_name)
        return getattr(mod, '%sHandler' % backend_name.capitalize())

    def handle_print(self, path_builder: PathBuilder):
        msg_parts = [
            '=[ DIRS ]=\n',
            '\tmanage.py: `%s`\n' % path_builder.get_manage_py_dir('.'),
            '\turlconf_dir: `%s`\n' % path_builder.urlconf_dir,
            '\tguessed_django_base_dir: `%s`\n' % path_builder.guessed_django_base_dir,
            '\tdjango_base_dir: `%s`\n' % path_builder.django_base_dir,
            '\tguessed_virtualenv_dir: `%s`\n' % path_builder.guessed_virtualenv_dir,
            '\tvirtualenv_dir: `%s`\n' % path_builder.virtualenv_dir,
            '\tvar_log_dir: `%s`\n' % path_builder.var_log_dir,
            '=[ NAMES ]=\n',
            '\tproject_name: `%s`\n' % path_builder.project_name,
            '\tdjango_sites: `%s`\n' % str(path_builder.django_sites),
            '\tguessed_site_name: `%s`\n' % path_builder.guessed_site_name,
            '\tsite_name: `%s`\n' % path_builder.site_name,
            '\tgunicorn_wsgi_application: `%s`\n' % path_builder.gunicorn_wsgi_application,
            '\tguess_virtualenv_python_executable: `%s`\n' % path_builder.guess_virtualenv_python_executable,
            '\tvirtualenv_python_executable: `%s`\n' % path_builder.virtualenv_python_executable,
            '\tgunicorn_executable: `%s`\n' % path_builder.gunicorn_executable,
            '\tsite_port: `%s`\n' % path_builder.site_port,
        ]
        return ''.join(msg_parts)

    def handle(self, *args, **options):
        pb = self.get_path_builder()()
        if options.get('print'):
            return self.handle_print(pb)

        backend_name = options.get('backend')
        try:
            data = self.get_handler(backend_name)(pb).render()
        except ModuleNotFoundError:
            try:
                data = GenericHandler(pb, template=backend_name).render()
            except TemplateDoesNotExist:
                data = GenericHandler(pb, template='django_congen/%s' % backend_name).render()

        self.stdout.write(data)
