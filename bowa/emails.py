# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-

"""Send emails (using a Celery task)."""

# Python 3 is coming
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import datetime
import json
import logging

from django import template
from django.core import mail
from django.core import urlresolvers
from django.template import loader
from django.contrib.sites.models import Site

from lizard_task.models import SecuredPeriodicTask

from . import models


def send_email_to_task(
    scenario_id, mail_template, subject, username='admin',
    email="", extra_context=None):
    """
    Create a task for sending email
    """
    taskname = 'BOWA Scenario ({}) send mail {}'.format(
        scenario_id, mail_template)
    task_kwargs = (
        '{{'
        '"username": "admin", '
        '"taskname": "{}", '
        '"scenario_id": "{}", '
        '"mail_template": "{}", '
        '"subject": "{}", '
        '"email": "{}", '
        '"extra_context": {} '
        '}}'
        ).format(taskname, scenario_id, mail_template,
                 subject, email,
                 "{}" if not extra_context else json.dumps(extra_context))
    email_task, created = SecuredPeriodicTask.objects.get_or_create(
        name=taskname, defaults={
            'kwargs': task_kwargs,
            'task': 'bowa.tasks.send_email'}
        )
    email_task.kwargs = task_kwargs
    email_task.task = 'bowa.tasks.send_email'
    email_task.save()
    email_task.send_task(username=username)


def do_send_email(
    scenario_id, username=None, taskname=None, loglevel=20,
    mail_template='email_received', subject='Onderwerp', email='',
    extra_context={}):
    """Called from the send_email task to actually send it."""

    logger = logging.getLogger(taskname)

    logger.info("send_mail: %s" % mail_template)
    scenario = models.BowaScenario.objects.get(pk=scenario_id)

    try:
        root_url = 'http://%s' % Site.objects.all()[0].domain
    except:
        root_url = 'http://test.schade.lizard.net'
        logger.error('Error fetching Site... defaulting')
    context = template.Context(
        {"scenario": scenario, 'ROOT_URL': root_url})
    context.update(extra_context)

    template_text = loader.get_template(
        "bowa/%s.txt" % mail_template)
    template_html = loader.get_template(
        "bowa/%s.html" % mail_template)

    from_email = 'no-reply@nelen-schuurmans.nl'
    if not email:
        # Default
        to = scenario.email
    else:
        # In case of user provided email (errors)
        to = email

    logger.info("scenario: %s" % scenario)
    logger.info("sending e-mail to: %s" % to)
    msg = mail.EmailMultiAlternatives(
        subject, template_text.render(context), from_email, [to])
    msg.attach_alternative(template_html.render(context), 'text/html')
    msg.send()

    logger.info("e-mail has been successfully sent")


def send_success_mail(scenario, username, logger, start_dt):
    """Send success mail"""
    logger.info('STATS BOWA scenario van %s is klaar in %r' % (
            scenario.email,
            str(datetime.datetime.now() - start_dt)))
    logger.info("creating email task for scenario %d" % scenario.id)
    subject = (
        'BOWA: Resultaten beschikbaar voor scenario %s '
        % scenario.name)
    send_email_to_task(
        scenario.id, 'email_success', subject, username=username)


def send_error_mail(scenario, username, logger, start_dt):
    # Send error mail
    logger.info('STATS BOWA scenario van %s is mislukt in %r' % (
            scenario.email,
            str(datetime.datetime.now() - start_dt)))
    logger.info("there were errors in scenario %d" % scenario.id)
    logger.info("creating email task for error")
    subject = (
        'BOWA: scenario %s heeft fouten'
        % scenario.name)
    send_email_to_task(
        scenario.id, 'email_error', subject, username=username)
