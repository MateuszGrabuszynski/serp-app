from celery import Celery, shared_task
from django.db import transaction

from serp_app import utils
from serp_app import models

app = Celery()


@shared_task
def query_google(query, no_results_to_return, user_agent, proxy, user_ip):
    if not user_agent or user_agent == '':
        config = models.Config.objects.first()
        user_agent = config.default_user_agent

    no_returned, results, h_stats, d_stats, hd_stats = utils.query_google(query,
                                                                          no_results_to_return=no_results_to_return,
                                                                          user_agent=user_agent, proxy=proxy)

    with transaction.atomic():
        search_object = models.Search.objects.create(query=query, user_ip=user_ip, no_returned_results=no_returned,
                                                     user_agent=user_agent, proxy_ip=proxy,
                                                     top_ten_words_headers=h_stats, top_ten_words_descriptions=d_stats,
                                                     top_ten_words_both=hd_stats,
                                                     task_id=query_google.request.id)

        curr_pos = 1
        for res in results:
            models.Result.objects.create(search_id=search_object, header=res[0], link=res[1], description=res[2],
                                         position=curr_pos)
            curr_pos += 1

    return True
