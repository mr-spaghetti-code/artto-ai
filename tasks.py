import os
import time
import random

from utils import create_app
from celery import shared_task


# from celery import Celery
from celery.utils.log import get_task_logger
from asgiref.sync import async_to_sync


from helpers.utils import *
from helpers.llm_helpers import *
from helpers.nft_data_helpers import *
from helpers.farcaster_helpers import *
from helpers.coinbase_helpers import *

from cron_tasks import *
from webhook_tasks import *


flask_app = create_app()  #-Line 2
celery_app = flask_app.extensions["celery"] #-Line 3

logger = get_task_logger(__name__)

@shared_task(ignore_result=False, name="post_channel_casts")
def sync_post_channel_casts():
    async_to_sync(post_channel_casts)()

@shared_task(ignore_result=False, name="post_thought_about_feed")
def sync_post_thought_about_feed():
    async_to_sync(post_thought_about_feed)()

@shared_task(ignore_result=False, name="post_thought")
def sync_post_thought():
    async_to_sync(post_thought)()

@shared_task(ignore_result=False, name="post_following_casts")
def sync_post_following_casts():
    async_to_sync(post_following_casts)()

@shared_task(ignore_result=False, name="post_trending_nfts")
def sync_post_trending_nfts():
    async_to_sync(post_trending_nfts)()

@shared_task(ignore_result=False, name="process_webhook")
def sync_process_webhook(webhook_data):
    async_to_sync(process_webhook)(webhook_data)

@shared_task(ignore_result=False, name="process_neynar_webhook")
def sync_process_neynar_webhook(webhook_data):
    async_to_sync(process_neynar_webhook)(webhook_data)



@shared_task(ignore_result=False, name="add")
def add(x, y):
    logger.info(f'Adding {x} + {y}')
    return x + y