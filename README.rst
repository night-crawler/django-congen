Installation
------------
.. code:: bash

    pip install -e git+https://github.com/night-crawler/django-congen.git@#egg=django-congen


Sample
------

Add `django-congen` to `INSTALLED_APPS`.


.. code:: bash

    # print collected settings
    ./manage.py congen -p

    # render nginx template with collected settings
    ./manage.py congen -b nginx

    # render django template with collected settings
    ./manage.py congen -b /path/to/template.conf
