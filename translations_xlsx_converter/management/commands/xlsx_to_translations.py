from django.core.management import BaseCommand

import logging

from translations_xlsx_converter import helpers, import_main

logging.basicConfig(level=logging.WARNING)


class Command(BaseCommand):
    help = "Import translations from Excel .xlsx file to Django .po files"

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "--use_db",
    #         action="store_true",
    #         help="Populate database table instead of creating .xlsx file. This database table can be then exported to .xlsx file manually. "
    #              "IMPORTANT - only ru, en and uz languages are currently supported for this option.",
    #     )

    def handle(self, *args, **options):
            self.stdout.write(
                self.style.SUCCESS('Starting import from Excel...')
            )

            import_main.convert_xlsx_to_po()

            self.style.SUCCESS('Translation files updated')
