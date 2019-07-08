from django import urls
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import edit, detail

from serp_app import models, forms, tasks


class QueryResults(detail.DetailView):
    model = models.Search


class NormalQueryView(edit.FormView):
    # model = models.Search
    form_class = forms.NormalQueryForm
    template_name = 'serp_app/normal_query.html'

    # success_url = '.'  # self

    def form_valid(self, form, *args, **kwargs):
        # get the data from request and form
        user_ip = self.request.META.get('HTTP_X_FORWARDED_FOR',
                                        self.request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
        query = form.cleaned_data['query']
        no_rtr = form.cleaned_data['no_results_to_return']
        ua = form.cleaned_data['user_agent']
        proxy = form.cleaned_data['proxy_ip']

        # clean the data
        if not ua or ua == '':
            ua = models.Config.objects.first().default_user_agent
        if not proxy or proxy == '':
            proxy = None

        # check cache
        caching_time = models.Config.objects.first().cache_time_limit
        ts_gt = timezone.localtime() - timezone.timedelta(seconds=caching_time)

        element = models.Search.objects.filter(query=query, user_agent=ua, proxy_ip=proxy,
                                               user_ip=user_ip, timestamp__gt=ts_gt)

        if element:  # use cache
            print('Returned result from cache!')
            tag = element.first().pk
        else:  # make the query
            tag = 0  # FIXME: this aint working for sure...
            tasks.query_google(query, no_rtr, ua, proxy, user_ip)
            # print(f'From the outside of the task... {tag}')
        self.success_url = urls.reverse('serp_app:search_results', kwargs={'query': tag})

        return super().form_valid(form)
