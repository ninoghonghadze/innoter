from datetime import date

from celery import shared_task

from .models import Page


@shared_task
def unblock_expired_pages():
    today = date.today()
    Page.objects.filter(is_blocked=True, unblock_date__lte=today).update(
        is_blocked=False, unblock_date=None
    )
