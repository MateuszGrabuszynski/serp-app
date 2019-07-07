from celery import Celery, shared_task

from serp_app import utils
from serp_app import models

app = Celery()


@shared_task
def query_google(query, user_ip, no_results_to_return=10, user_agent='', proxy=''):
    # TODO: set default user_agent or return it from utils.query_google()
    no_results, results = utils.query_google(query, no_results_to_return, user_agent, proxy)
    models.Search.objects.create(
        query=query, user_ip=user_ip, no_returned_results=no_results, user_agent=user_agent
    )
    return True
