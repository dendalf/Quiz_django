from sys import stdout

from celery import shared_task
from celery.utils.log import get_task_logger

from django.core.management import call_command
from django.utils import timezone

from prettytable import PrettyTable

from quiz.models import Result

logger = get_task_logger(__name__)


@shared_task
def simple_task():
    logger.info('>>> Simple Task <<<')


@shared_task
def send_email_report():
    call_command('send_report')


@shared_task
def send_email_reminder():
    results = Result.objects.filter(create_timestamp__lt=timezone.now(), state=0)

    if results:
        tab = PrettyTable()
        tab.field_names = ['Test', 'Date of start']

        for result in results:
            tab.add_row([
                result.exam.title,
                result.create_timestamp
            ])

            subj = 'Finish your pending tests!'
            result.user.email_user(subj, tab.get_string())
            stdout.write('The report was sent by the admins email')

    else:
        stdout.write('Nothing to send')
