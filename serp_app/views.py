from django import urls
from django.http import HttpResponse
from django.utils import timezone
from django.views import View
from django.views.generic import edit, detail
from django.shortcuts import redirect

from serp_app import models, forms, tasks


class QueryResults(detail.DetailView):
    model = models.Search


class QueryResultsByTask(View):
    def get(self, request, *args, **kwargs):
        task_id = kwargs['task_id']

        check = models.Search.objects.filter(task_id=task_id)

        if check:
            return redirect(urls.reverse('serp_app:search_results', kwargs={'pk': check.first().pk}))
        else:
            qstring = request.GET.urlencode()
            timeout_pos = qstring.find('timeout=')
            if timeout_pos > 0:
                timeout_end = qstring[timeout_pos + 8:].find('&')
                if timeout_end > 0:
                    timeout = int(qstring[timeout_pos + 8:timeout_pos + 8 + timeout_end])
                else:
                    timeout = int(qstring[timeout_pos + 8:])
            else:
                timeout = 2

            if timeout < 10:
                timeout += 2
            else:
                timeout += 10

            reverse_url = f"{urls.reverse('serp_app:search_results_by_task', kwargs={'task_id': task_id})}?timeout={timeout}"
            html = f'''
                <html><head><meta http-equiv="refresh" content="{timeout}; url={reverse_url}"></head><body>Please wait. Your results are being prepared.
                If the page does not reload, <a href="{reverse_url}">click here</a></body></html>
            '''
            return HttpResponse(html, status=202)


class NormalQueryView(edit.FormView):
    form_class = forms.NormalQueryForm
    template_name = 'serp_app/normal_query.html'

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
            pk_num = element.first().pk
            self.success_url = urls.reverse('serp_app:search_results', kwargs={'pk': pk_num})
        else:  # make the query
            task_id = tasks.query_google.delay(query, no_rtr, ua, proxy, user_ip)
            self.success_url = urls.reverse('serp_app:search_results_by_task', kwargs={'task_id': task_id})

        return super().form_valid(form)
