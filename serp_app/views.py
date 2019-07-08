from django import urls
from django.http import HttpResponse
from django.utils import timezone
from django.views import View
from django.views.generic import edit, detail, list
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
            retry = 1

            try:
                qs = request.GET.urlencode()
                qs_spl = qs.split("=")
                if qs_spl[0] == 'retry':
                    retry = int(qs_spl[1])
            except Exception:
                pass

            reverse_url = f"{urls.reverse('serp_app:search_results_by_task', kwargs={'task_id': task_id})}?retry={retry+1}"
            html = f'''
                <html><head><meta http-equiv="refresh" content="{retry + 2 if retry < 5 else retry*5}; url={reverse_url}"></head>
                <body>Please wait. Your results are being prepared.
                If the page does not reload, <a href="{reverse_url}">click here</a>.
                If you want to cancel, <a href="{urls.reverse('serp_app:latest_searches')}">click here</a>.</body></html>
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


class LatestSearchesView(list.ListView):
    model = models.Search
    context_object_name = 'searches'
