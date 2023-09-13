from django.core.management import BaseCommand

import logging

from translations_xlsx_converter import helpers, export_main

logging.basicConfig(level=logging.WARNING)


class Command(BaseCommand):
    help = "Convert all Django translation .po files to single Excel .xlsx file"

    def add_arguments(self, parser):
        parser.add_argument(
            "--use_db",
            action="store_true",
            help="Populate database table instead of creating .xlsx file. This database table can be then exported to .xlsx file manually. "
                 "IMPORTANT - only ru, en and uz languages are currently supported for this option.",
        )

    def handle(self, *args, use_db=False, **options):
            self.stdout.write(
                self.style.SUCCESS('Starting Excel conversion...')
            )

            export_main.convert_po_to_xlsx(use_db)

            self.style.SUCCESS('Translation files converted to .xlsx')
