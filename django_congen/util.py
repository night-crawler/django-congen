# -*- coding: utf-8 -*-
import os
import sys

from importlib import import_module
from django.conf import settings as django_settings
from django.utils.functional import cached_property

from .settings import MAX_DEPTH

import django_congen


def find_file_flat(filename, path, is_dir=False):
    """No recursion, flat search
    :param filename: file being searched
    :param path: scan path
    :param is_dir: find dirs or files
    :return: None or found filepath
    """
    items = os.listdir(path)
    # print path, files
    if filename in items:
        file_path = os.path.join(path, filename)
        if is_dir == os.path.isdir(file_path):
            return file_path
        return None

    return None


def find_file_in_parents(name, start_path, is_dir=False):
    """
    Walking by uptree
    :param name: needle
    :param start_path: a path where lookup starts
    :param is_dir: find dirs or files
    :return: path to found file or None
    """
    start_path = os.path.abspath(start_path)
    depth = MAX_DEPTH
    while depth >= 0:
        res = find_file_flat(name, start_path, is_dir)
        depth -= 1
        if not res:
            start_path = os.path.dirname(start_path)
            continue
        return res

    return None


class SettingsWrapper(object):
    def __getattr__(self, item):
        return getattr(django_settings, item, None)

s = SettingsWrapper()


class PathBuilder(object):

    def get_manage_py_dir(self, start_path):
        """
        :param start_path: start lookup of a file `manage.py` from this path
        :return: "/var/www/<example.com>/project" - where example.com is a site name and it's virtualenv
        """
        manage_py_file = find_file_in_parents('manage.py', start_path)
        return os.path.dirname(manage_py_file)

    @cached_property
    def project_name(self):
        """
        Get Django project name from variable in settings, or via first part of WSGI_APPLICATION
        :return: "django_project"
        """
        return s.PROJECT_NAME or s.WSGI_APPLICATION.split('.')[0]

    @cached_property
    def urlconf_dir(self):
        """
        Gets directory where ROOT_URLCONF file stored
        :return: "/var/www/<example.com>/project/project" - where example.com is a site name and it's virtualenv
        """
        urlconf_mod = import_module(django_settings.ROOT_URLCONF)
        urlconf_path = os.path.dirname(os.path.abspath(urlconf_mod.__file__))
        return urlconf_path

    @cached_property
    def guessed_django_base_dir(self):
        """
        Guesses Django project `BASE_DIR` by `ROOT_URLCONF`.
        :return: "/var/www/<example.com>/project" - where example.com is a site name and it's virtualenv
        """
        return self.get_manage_py_dir(self.urlconf_dir)

    @cached_property
    def django_base_dir(self):
        """
        Gets
        :return: "/var/www/<example.com>/project" - where example.com is a site name and it's virtualenv
        """
        base_dir = s.BASE_DIR or self.guessed_django_base_dir
        return base_dir

    @cached_property
    def guessed_virtualenv_dir(self):
        """
        Detect virtualenv dir by `os` module path
        :return: "/var/www/<example.com>" - site name && venv
        """
        os_path = os.path.abspath(os.path.dirname(os.__file__))
        virtualenv_dir = os.path.abspath(os.path.join(os_path, os.pardir, os.pardir))

        # Django project folder should be in the virtualenv, otherwise raise
        # check it stupidly, it's better to fail that provide a wrong result
        # if not self.django_base_dir.startswith(virtualenv_dir):
        #     raise Exception('It seems virtualenv is not active: \n'
        #                     'BASE_DIR="%s"\n'
        #                     'VIRTUALENV_DIR="%s"' % (self.django_base_dir, virtualenv_dir))

        return virtualenv_dir

    @cached_property
    def virtualenv_dir(self):
        """
        Get virtualenv dir from settings, or as `os.environ['VIRTUAL_ENV']` variable, or guess
        :return: "/var/www/<example.com>" - site name && venv
        """

        return s.VIRTUAL_ENV_DIR or os.environ.get('VIRTUAL_ENV', self.guessed_virtualenv_dir)

    @cached_property
    def django_sites(self):
        """
        Get available sites from `django.contrib.sites`
        :return: all sites queryset
        """
        try:
            from django.contrib.sites.models import Site
            return Site.objects.all()
        except RuntimeError:
            return ''

    @cached_property
    def guessed_site_name(self):
        """
        Guess site name by virtualenv directory
        :return:
        """
        return os.path.basename(self.virtualenv_dir)

    @cached_property
    def site_name(self):
        """
        Get site name from Django `settings` module, then get it with `django.contrib.sites`,
        or guess by virtualenv directory name
        :return: "project"
        """
        site_name = s.SITE_NAME
        if not site_name and 'django.contrib.sites' in django_settings.INSTALLED_APPS:
            site_name = self.django_sites.get(pk=django_settings.SITE_ID).name

        return site_name or self.guessed_site_name

    @cached_property
    def var_log_dir(self):
        """
        Get project logging directory in /var/log/
        :return: "/var/log/project"
        """
        return os.path.join('/var/log/', self.site_name)

    @cached_property
    def gunicorn_wsgi_application(self):
        """
        Get project wsgi in gunicorn argument format
        :return: "project.wsgi:application"
        """
        wsgi_path = tuple(django_settings.WSGI_APPLICATION.split('.'))
        return '%s.%s:%s' % wsgi_path

    @cached_property
    def guess_virtualenv_python_executable(self):
        """
        Guess virtualenv python executable by guessed virtualenv dir
        :return:
        """
        return os.path.join(self.virtualenv_dir, 'bin', 'python')

    @cached_property
    def virtualenv_python_executable(self):
        """
        Get virtualenv python, believe script starts from activated virtualenv
        :return:
        """
        path = None

        virtualenv_dir = os.environ.get('VIRTUAL_ENV', None)
        if virtualenv_dir:
            path = sys.executable

        if not path:
            path = self.guess_virtualenv_python_executable

        return path

    @cached_property
    def gunicorn_executable(self):
        """

        :return:
        """
        return s.GUNICORN_EXECUTABLE or os.path.join(self.virtualenv_dir, 'bin', 'gunicorn')


    @cached_property
    def site_port(self):
        """
        :return: site port from settings
        """
        return s.SITE_PORT or None
