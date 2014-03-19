import logging

from django.core.management.base import BaseCommand

from bowa import models

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = '<scenario_id>'
    help = 'Start de berekening van een scenario'

    def handle(self, *args, **options):
        scenario_id = args[0]

        scenario = models.BowaScenario.objects.get(pk=scenario_id)
        scenario.run_r(logger)

        self.stdout.write("OK.\n")
