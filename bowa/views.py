# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function


# from django.utils.translation import ugettext as _
# from django.core.urlresolvers import reverse
# from lizard_map.views import MapView

import logging

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

from django.views.generic import TemplateView
from django.http import Http404
from django.http import HttpResponseRedirect
from django.http import HttpResponse

from lizard_ui.views import ViewContextMixin
from lizard_ui.views import UiView

from bowa import forms
from bowa import models
from bowa import tools
from bowa import tasks

logger = logging.getLogger(__name__)


class HomeView(UiView):
    template_name = "bowa/home.html"

    def get(self, request):
        self.scenario_form = forms.ScenarioForm()

        return super(HomeView, self).get(request)

    def post(self, request):
        self.scenario_form = forms.ScenarioForm(request.POST, request.FILES)

        if not self.scenario_form.is_valid():
            self.scenario_form.remove_tempdir()
            return super(HomeView, self).get(request)

        scenario = models.BowaScenario.objects.create(
            name=self.scenario_form.cleaned_data['name'],
            email=self.scenario_form.cleaned_data['email'],
            ahdev=self.scenario_form.cleaned_data['ahdev'],
            htdev=self.scenario_form.cleaned_data['htdev'],
            nsim=self.scenario_form.cleaned_data['nsim'],
            scenario_type=self.scenario_form.cleaned_data['scenario_type'])

        scenario.move_files(self.scenario_form.metadata)
        self.scenario_form.remove_tempdir()


	tasks.create_task_for(scenario)

        return HttpResponseRedirect(scenario.get_absolute_url())


    def version(self):
        return tools.version()


class BowaScenarioResult(UiView):
    template_name = "bowa/result.html"
    active_menu = "table"

    def get(self, request, slug):
        try:
            self.result = models.BowaScenario.objects.get(slug=slug)
        except models.BowaScenario.DoesNotExist:
            raise Http404()

        return super(BowaScenarioResult, self).get(request)


class BowaScenarioResultMap(BowaScenarioResult):
    template_name = "bowa/result_map.html"
    active_menu = "map"


class BowaScenarioResultGraph(BowaScenarioResult):
    template_name = "bowa/result_graph.html"
    active_menu = "graph"


class Disclaimer(ViewContextMixin, TemplateView):
    template_name = 'bowa/disclaimer.html'

    def version(self):
        return tools.version()


def result_graph_image(request, slug):
    try:
        scenario = models.BowaScenario.objects.get(slug=slug)
    except models.BowaScenario.DoesNotExist:
        raise Http404()

    toetseenheid = request.GET.get('toetseenheid')
    grondgebruik = request.GET.get('grondgebruik')
    normfunctie = request.GET.get('normfunctie')

    logger.debug('Toetseenheid : ' + toetseenheid)
    logger.debug('Grondgebruik : ' + grondgebruik)
    logger.debug('Normfunctie : ' + normfunctie)

    # Result lines
    wateropgave = scenario.resultline_set.filter(
        toetseenheid=toetseenheid,
        functie=grondgebruik,
        percentage__gt=0)

    data = wateropgave.values(normfunctie)

    logger.debug('wateropgave : ' + str(len(data)))
    titel = 'Toetseenheid ' + toetseenheid + ':' + grondgebruik

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1,axisbg='white')

    x = np.random.normal(0,1,1000)
    numbins = 50
    ax.hist(x,numbins,color='green',alpha=0.8) 

    ax.set_xlabel(normfunctie)
    ax.set_ylabel('Aantal simulaties [-]')
    ax.set_title(titel)

    canvas = FigureCanvas(fig)

    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response


def result_map_image(request, slug):
    try:
        scenario = models.BowaScenario.objects.get(slug=slug)
    except models.BowaScenario.DoesNotExist:
        raise Http404()

    presentatie = request.GET.get('presentatie')
    grondgebruik = request.GET.get('grondgebruik')
    normfunctie = request.GET.get('normfunctie')

    logger.debug('Presentatie : ' + presentatie)
    logger.debug('Grondgebruik : ' + grondgebruik)
    logger.debug('Normfunctie : ' + normfunctie)

    response = HttpResponse(content_type='image/png')
    return response
