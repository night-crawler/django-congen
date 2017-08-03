from setuptools import setup, find_packages
from django_congen import __version__


with open('README.rst', 'r') as f:
    long_description = f.read()


setup(
    name='django-congen',
    version=__version__,
    packages=find_packages(),
    url='https://github.com/night-crawler/django-congen',
    license='MIT',
    author='night-crawler',
    author_email='lilo.panic@gmail.com',
    description='Django CONfig GENerator',
    long_description=long_description,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
    ],
    requires=['django']
)
