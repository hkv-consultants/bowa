# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function


# from django.utils.translation import ugettext as _
# from django.core.urlresolvers import reverse
# from lizard_map.views import MapView

from django.http import Http404
from django.http import HttpResponseRedirect

from lizard_ui.views import UiView

from bowa import forms
from bowa import models
from bowa import tools


class HomeView(UiView):
    template_name = "bowa/home.html"

    def get(self, request):
        self.scenario_form = forms.ScenarioForm()

        return super(HomeView, self).get(request)

    def post(self, request):
        self.scenario_form = forms.ScenarioForm(request.POST)

        if not self.scenario_form.is_valid():
            return super(HomeView, self).get(request)

        scenario = models.BowaScenario.objects.create(
            name=self.scenario_form.cleaned_data['name'],
            email=self.scenario_form.cleaned_data['email'])

        return HttpResponseRedirect(scenario.get_absolute_url())

    def version(self):
        return tools.version()


class BowaScenarioResult(UiView):
    template_name = "bowa/result.html"

    def get(self, request, slug):
        try:
            self.result = models.BowaScenario.objects.get(slug=slug)
        except models.BowaScenario.DoesNotExist:
            raise Http404()

        return super(BowaScenarioResult, self).get(request)

