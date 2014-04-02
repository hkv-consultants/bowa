import datetime
import json
import logging
import sys
import traceback

from celery.task import task
from lizard_task.models import SecuredPeriodicTask
from lizard_task.task import task_logging

from bowa import models
from bowa import emails


def create_task_for(scenario, username="admin"):
    # Create database object for this task
    taskname = 'BOWA Scenario id={}'.format(scenario.id)
    task_kwargs = json.dumps({
        'scenario_id': scenario.id,
        'taskname': taskname
        })
    run_scenario_task, created = SecuredPeriodicTask.objects.get_or_create(
        name=taskname)
    run_scenario_task.kwargs = task_kwargs
    run_scenario_task.task = 'bowa.tasks.run_scenario'
    run_scenario_task.save()

    # Run it asynchronously
    run_scenario_task.send_task(username=username)


@task
@task_logging
def run_scenario(scenario_id, taskname, username):
    """Retrieve scenario from the database and run it."""
    logger = logging.getLogger(taskname)
    logger.info("calculate damage")

    start_dt = datetime.datetime.now()
    try:
        scenario = models.BowaScenario.objects.get(pk=scenario_id)
        scenario.run_r(logger)
        scenario.create_inundation_png()
        emails.send_success_mail(scenario, "admin", logger, start_dt)
    except:
        exc_info = sys.exc_info()
        traceback.print_exception(*exc_info, limit=None)
        emails.send_error_mail(scenario, "admin", logger, start_dt)
        return 'failure'


@task
@task_logging
def send_email(scenario_id, username=None, taskname=None, loglevel=20,
               mail_template='email_received', subject='Onderwerp', email='',
               extra_context={}):
    return emails.do_send_email(
        scenario_id, username, taskname, loglevel,
        mail_template, subject, email, extra_context)
