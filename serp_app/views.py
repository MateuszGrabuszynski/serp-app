from django.shortcuts import render
from django.views.generic import edit

from serp_app import models, forms, tasks


class NormalQueryView(edit.CreateView):
    model = models.Search
    form_class = forms.NormalQueryForm
    template_name = 'serp_app/normal_query.html'
    success_url = '.'  # self

    def form_valid(self, form, *args, **kwargs):
        print('Form valid')
        form.instance.user_ip = self.request.META.get('HTTP_X_FORWARDED_FOR',
                                                      self.request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
        info = tasks.query_google.delay(form.instance.query,
                                        no_results_to_return=form.instance.no_returned_results,
                                        user_agent=form.instance.user_agent,
                                        proxy=form.instance.proxy_ip)
        print('INFO: ', info)
        return super().form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
    #     return super().post(request, *args, **kwargs)
    #     # tasks.query_google()
