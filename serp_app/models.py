from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Proxy(models.Model):
    name = models.CharField(max_length=20)
    ip = models.GenericIPAddressField()
    port = models.IntegerField(default=80, validators=[MinValueValidator(1), MaxValueValidator(65535)])
    country = models.CharField(default='unknown', max_length=255)


class Config(models.Model):
    name = models.CharField(max_length=20)
    cache_time_limit = models.IntegerField(validators=[MinValueValidator(0)])  # 0 = don't cache
    default_user_agent = models.TextField()

    def __str__(self):
        return f'{self.name} config'


class Search(models.Model):
    query = models.TextField()
    user_ip = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    no_returned_results = models.IntegerField()
    user_agent = models.TextField()
    proxy_ip = models.GenericIPAddressField(null=True, blank=True)

    # JSON formatted table, i.e. [["word", frequency], ["word", frequency]...]
    top_ten_words_headers = models.TextField(null=True, blank=True)
    top_ten_words_descriptions = models.TextField(null=True, blank=True)
    top_ten_words_both = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Searches'

    def __str__(self):
        return f'Query \"{self.query}\" from user {self.user_ip}'


class Result(models.Model):
    search_id = models.ForeignKey(Search, on_delete=models.CASCADE, related_name='results')
    header = models.TextField()
    link = models.URLField()
    description = models.TextField()
    position = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f'{self.position}. {self.header} for search {self.search_id}'
