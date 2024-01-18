from django.conf import settings
from translations_xlsx_converter import helpers

LOCALE_PATH = "locale"

try:
    TRANSLATIONS_EXCEL_FILE_NAME = settings.TRANSLATIONS_EXCEL_FILE_NAME
except AttributeError:
    TRANSLATIONS_EXCEL_FILE_NAME = "translations.xlsx"


def convert_xlsx_to_po(xlsx_location=None):
    languages = helpers.get_languages(LOCALE_PATH)
    po_file_location_objects = [
        dict(
            location=f"{LOCALE_PATH}/{language}/LC_MESSAGES/django.po",
            language=language
        ) for language in languages
    ]

    po_file_objects_list = [
        dict(
            file=helpers.read_po(path_obj["location"]),
            language=path_obj["language"]
        ) for path_obj in po_file_location_objects
    ]

    if not xlsx_location:
        xlsx_location = f"{LOCALE_PATH}/{TRANSLATIONS_EXCEL_FILE_NAME}"

    dict_from_excel = helpers.get_dict_from_excel(xlsx_location, languages)

    for po_file_object in po_file_objects_list:
        source_pofile = po_file_object["file"]
        language = po_file_object["language"]

        helpers.update_source(source_pofile, language, dict_from_excel)
        source_pofile.save()
