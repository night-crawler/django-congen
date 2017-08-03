import multiprocessing

bind = ['127.0.0.1:{{ path.site_port }}', 'unix:{{ path.virtualenv_dir}}/run/gunicorn.sock']
workers = multiprocessing.cpu_count()
pid = '{{ path.virtualenv_dir}}/pid/gunicorn.pid'
reload = True
preload_app = True
chdir = '{{ path.virtualenv_dir}}/{{ path.project_name }}'
pythonpath = '{{ path.virtualenv_python_executable }}'
raw_env = [
    'DJANGO_SETTINGS_MODULE={{ path.project_name }}.settings',
    'LANG=ru_RU.UTF-8',
    'LC_ALL=ru_RU.UTF-8',
    'LC_LANG=ru_RU.UTF-8'
]
user = '{{ path.project_name }}'
group = '{{ path.project_name }}'
errorlog = '{{ path.var_log_dir }}/gunicorn-error.log'
timeout = 10
