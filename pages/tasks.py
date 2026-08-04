from datetime import date
from celery import shared_task
from .models import Page
import logging

logger = logging.getLogger(__name__)

@shared_task
def unblock_expired_pages():
    today = date.today()
    count = Page.objects.filter(is_blocked=True, unblock_date__lte=today).count()
    Page.objects.filter(is_blocked=True, unblock_date__lte=today).update(
        is_blocked=False, unblock_date=None
    )
    logger.info(f"Unblocked {count} pages on {today}")

@shared_task
def unblock_expired_pages():
    today = date.today()
    Page.objects.filter(is_blocked=True, unblock_date__lte=today).update(
        is_blocked=False, unblock_date=None
    )
