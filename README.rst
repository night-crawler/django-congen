Installation
------------
.. code:: bash

    pip install -e git+https://github.com/night-crawler/django-congen.git@#egg=django-congen


Sample
------

Add `django-congen` to `INSTALLED_APPS`.


.. code:: bash

    ./manage.py congen -b nginx
    ./manage.py congen -b /path/to/template.conf

