from django.db import models


class Search(models.Model):
    search = models.CharField(max_length=500)
    created_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'f{self.search}'

    # without the next 2 lines the plural form of search will be shown as searchs
    class Meta:
        verbose_name_plural = 'Searches'
