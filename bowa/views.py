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

import matplotlib.pyplot as plt

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
    logger.debug('Normfuntie : ' + normfuntie)

    # Result lines
    wateropgave = scenario.resultline_set.filter(
        toetseenheid=toetseenheid,
        grondgebruik=grondgebruik,
        percentage__gt=0)

    # Maak matplotlib grafiek
    titel = 'Toetseenheid ' + toetseenheid + ':' + grondgebruik
    logger.debug('Titel : ' + titel)

    mu, sigma = 100, 15
    x = mu + sigma * np.random.randn(10000)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    # the histogram of the data
    n, bins, patches = ax.hist(x, 50, normed=1, facecolor='green', alpha=0.75)

    # hist uses np.histogram under the hood to create 'n' and 'bins'.
    # np.histogram returns the bin edges, so there will be 50 probability
    # density values in n, 51 bin edges in bins and 50 patches.  To get
    # everything lined up, we'll compute the bin centers
    bincenters = 0.5*(bins[1:]+bins[:-1])
    # add a 'best fit' line for the normal PDF
    y = mlab.normpdf( bincenters, mu, sigma)
    l = ax.plot(bincenters, y, 'r--', linewidth=1)

    ax.set_xlabel('Smarts')
    ax.set_ylabel('Probability')
    #ax.set_title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
    ax.set_xlim(40, 160)
    ax.set_ylim(0, 0.03)
    ax.grid(True)

    plt.show()

    canvas = FigureCanvas(fig)

    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response
