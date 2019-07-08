from django import forms


class NormalQueryForm(forms.Form):
    query = forms.CharField()
    no_results_to_return = forms.IntegerField()
    user_agent = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 20}), required=False, help_text="Default UA will be used if empty")
    proxy_ip = forms.GenericIPAddressField(required=False, help_text="No proxy will be used if empty")
