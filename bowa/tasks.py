import json
import logging
import sys
import traceback

from celery.task import task
from lizard_task.models import SecuredPeriodicTask
from lizard_task.task import task_logging

from bowa import models


def create_task_for(scenario, username="admin"):
    # Create database object for this task
    task_name = 'BOWA Scenario id={}'.format(scenario.id)
    task_kwargs = json.dumps({
        'scenario_id': scenario.id,
        'task_name': task_name
        })
    run_scenario_task, created = SecuredPeriodicTask.objects.get_or_create(
        name=task_name)
    run_scenario_task.kwargs = task_kwargs
    run_scenario_task.task = 'bowa.tasks.run_scenario'
    run_scenario_task.save()

    # Run it asynchronously
    run_scenario_task.send_task(username=username)


@task
@task_logging
def run_scenario(scenario_id, task_name, username):
    """Retrieve scenario from the database and run it."""
    logger = logging.getLogger(task_name)
    logger.info("calculate damage")

    try:
        scenario = models.BowaScenario.objects.get(pk=scenario_id)
        scenario.run_r(logger)
    except:
        exc_info = sys.exc_info()
        traceback.print_exception(*exc_info, limit=None)
        return 'failure'
