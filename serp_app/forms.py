from django import forms

from serp_app import models


class NormalQueryForm(forms.ModelForm):
    class Meta:
        model = models.Search
        fields = ('query', 'user_ip', 'no_returned_results', 'user_agent', 'proxy_ip')

