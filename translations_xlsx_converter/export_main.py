from django.conf import settings

from translations_xlsx_converter import helpers
from translations_xlsx_converter.models import TranslationsXlsxConverter

LOCALE_PATH = "locale"

try:
    SERVICE_NAME_FOR_TRANSLATIONS_ORIGIN = settings.SERVICE_NAME_FOR_TRANSLATIONS_ORIGIN
except AttributeError:
    SERVICE_NAME_FOR_TRANSLATIONS_ORIGIN = "unknown"

try:
    TRANSLATIONS_EXCEL_FILE_NAME = settings.TRANSLATIONS_EXCEL_FILE_NAME
except AttributeError:
    TRANSLATIONS_EXCEL_FILE_NAME = "translations.xlsx"


def convert_po_to_xlsx(use_db):
    languages_list = helpers.get_languages(LOCALE_PATH)
    if use_db:
        return _populate_translations_db_table(languages_list)

    language_nested_messages_dict = _get_language_nested_dict(languages_list)
    helpers.write_messages_to_excel(f"{LOCALE_PATH}/{TRANSLATIONS_EXCEL_FILE_NAME}", languages_list, language_nested_messages_dict)


def _get_language_nested_dict(languages_list):
    language_nested_dict = {}

    for language in languages_list:
        path_to_po_file = f"{LOCALE_PATH}/{language}/LC_MESSAGES/django.po"
        po_dict = helpers.po_to_dict(helpers.read_po(path_to_po_file))

        for translation_key in po_dict:
            translation_value_dict = language_nested_dict.get(translation_key, {})
            translation_value_dict[language] = po_dict[translation_key]

            language_nested_dict[translation_key] = translation_value_dict

    return language_nested_dict


def _populate_translations_db_table(language_list):
    language_nested_dict = _get_language_nested_dict(language_list)

    for key in language_nested_dict:
        translations = language_nested_dict[key]
        TranslationsXlsxConverter.objects.update_or_create(
            key=key,
            defaults={
                "ru": translations.get("ru", ""),
                "uz": translations.get("uz", ""),
                "en": translations.get("en", ""),
                "origin_service": SERVICE_NAME_FOR_TRANSLATIONS_ORIGIN,
            }
        )
