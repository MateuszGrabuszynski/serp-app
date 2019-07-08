from celery import Celery, shared_task

from serp_app import utils
from serp_app import models

app = Celery()


@shared_task
def query_google(query, no_results_to_return, user_agent, proxy, user_ip):
    print(f'From the inside of the task... {query_google.request.id}')
    info = f'query: {query} // no_res: {no_results_to_return} // ua: {user_agent} // proxy: {proxy} // ip: {user_ip}'
    obj_ = models.Search.objects.create(query=query,
                                        user_agent=user_agent,
                                        proxy_ip=proxy,
                                        user_ip=user_ip,
                                        top_ten_words_headers=query_google.request.id)
    # obj_.top_ten_headers = "lelki"
    obj_.save()


    # TODO: set default user_agent or return it from utils.query_google()
    # no_results, results = utils.query_google(query, no_results_to_return, user_agent, proxy)
    return True
