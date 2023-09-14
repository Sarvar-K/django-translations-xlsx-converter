Utility to convert Django .po files to Excel .xlsx file and vice-versa for Django projects
=======================
Library provides tools to:
- Generate Excel .xlsx file based on Django .po files
- Collect translatable strings from Django .po files to database table
- Update Django .po files from Excel .xlsx file

Installation
----------------
```commandline
 pip install git+https://github.com/Sarvar-K/django-translations-xlsx-converter
```

In _requirements.txt_ file
```txt
git+https://github.com/ksinn/django-microservices-communication
```
**Installation in Docker**: If installing via *pip install*, you will require *git* in image.

Setup
--------------
Add 'services_communication' to your INSTALLED_APPS in settings.py.
```python
INSTALLED_APPS = [
    ...
    'translations_xlsx_converter',
]
```

You can also add the following global settings to settings.py (defaults are listed in the example below):
```python
SERVICE_NAME_FOR_TRANSLATIONS_ORIGIN = "unknown"
TRANSLATIONS_EXCEL_FILE_NAME = "translations.xlsx"
```
Where:
- SERVICE_NAME_FOR_TRANSLATIONS_ORIGIN - name of the Django project. This setting is used to populate 
_origin_service_ column in database table when collecting translations to database.
- TRANSLATIONS_EXCEL_FILE_NAME - name of an Excel file to export and import translations to and from Django .po files.

Add _locale_ directory to your project on the _manage.py_ directory tree level. Add empty subdirectories to 
_locale_ directory with their names corresponding to the language codes of the translations. Both _en_ and *en_EN*
notations are supported. 

The _locale_ directory will hold both Django .po files and exported/imported Excel .xlsx 
 file. The resulting project directory tree should be similar to this:
```
some_project/
    | some_project/
    |    | settings.py
    |    | urls.py
    | some_app/
    |    | __init__.py
    |    | admin.py
    |    | apps.py
    |    | models.py
    |    | tests.py
    |    | viwes.py
    | __init.py__
    | manage.py
    | locale/ <-----------
    |    | ru/
    |    | en/
    |    | uz/
    ...
```


Usage
---------------------------------

Migrating
----------------
If using different postgresql schemas for different projects within the same database and the database table
_translations_xlsx_converter_ already exists, **simply --fake migration** with:
```commandline
python3 manage.py migrate translations_xlsx_converter --fake
```

Exporting from Django to Excel
----------------
**Run the following command to generate .xlsx file:**
```commandline
python3 manage.py translations_to_xlsx
```
Excel file will be generated from the .po files from respective _locale_ subdirectories and placed in the _locale_
directory.

Exporting from Django to database
----------------
Run migration if necessary and then **run the following command to populate database table:**
```commandline
python3 manage.py translations_to_xlsx --use_db
```
The 'default' database from _DATABASES_ settings key in _settings.py_ will be used for this operation. The 
translations from .po files will be collected to _translations_collector.translations_xlsx_converter_ (_schema.table_name_)
database table. 

If the translation key (#msgid) from .po file already exists in the database table and your wish to overwrite it,
add *--update* argument to the command like so:
```commandline
python3 manage.py translations_to_xlsx --use_db --update
```
Otherwise, this key will be skipped.

Currently, only **en, ru and uz** languages are supported for exporting to database.

Exporting from database to Excel
-----------------
Run the following SQL query in your database:
```sql
SELECT 
	txc."key",
	txc.ru,
	txc.uz,
	txc.en,
	txc.origin_service
FROM translations_collector.translations_xlsx_converter AS txc
ORDER BY id;
```
Export resulting dataset to Excel .xlsx file. Make sure to **only** include the rows of actual dataset in the export,
e.g. skip the table information row with the (key, ru, uz, en) cells.

Name the resulting .xlsx file in accordance with your TRANSLATIONS_EXCEL_FILE_NAME in _settings.py_ if it 
is set. Otherwise, name your .xlsx file as _translations.xlsx_.

Put your .xlsx file in your Django project's _locale_ directory.

Import translations from Excel to Django
----------
Make sure your Excel .xlsx file is in the root of _locale_ directory and **run the following command:**
```commandline
python3 manage.py xlsx_to_translations
```
Translations of the Django .po files in the _locale_ directory will be updated in accordance with the
provided Excel .xlsx file.