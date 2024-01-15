from distutils.core import setup

from setuptools import find_packages

setup(
    name='translations_xlsx_converter',
    version='0.0.8',
    packages=find_packages(),
    url='https://github.com/Sarvar-K/django-translations-xlsx-converter',
    author='Sarvar-K',
    author_email='sarvar.kamilov1@gmail.com',
    description='Utility to convert translations in Django .po files to Excel .xlsx file and vice-versa for services written on Django',
    long_description_content_type="text/markdown",
    install_requires=[
        "Django>=4.0.0",
        "polib>=1.2.0",
        "openpyxl>=3.1.0",
    ],
    setup_requires=['wheel'],
)
