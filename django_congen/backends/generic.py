from django.template.loader import render_to_string


class GenericHandler(object):
    template = 'django_congen/gunicorn_release.py'
    pb = None

    def __init__(self, path_builder_instance, template=None):
        self.pb = path_builder_instance

        if template:
            self.template = template

    def render(self):
        c = {'path': self.pb}
        return render_to_string(self.template, c)
