from django.db import models


class TranslationsXlsxConverter(models.Model):
    key = models.TextField(unique=True)
    ru = models.TextField()
    uz = models.TextField()
    en = models.TextField()
    origin_service = models.CharField(max_length=128)

    class Meta:
        db_table = 'translations_collector"."translations_xlsx_converter'
