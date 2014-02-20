from django import forms
import logging
from bowa.models import BowaScenario
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode


logger = logging.getLogger(__name__)


SCENARIO_TYPES = BowaScenario.SCENARIO_TYPES


class CustomRadioSelectRenderer(forms.RadioSelect.renderer):
    """ Modifies some of the Radio buttons to be disabled in HTML,
    based on an externally-appended Actives list. """
    def render(self):
        if not hasattr(self, "actives"):  # oops, forgot to add an Actives list
            return self.original_render()
        return self.my_render()

    def original_render(self):
        return mark_safe(u'<ul>\n%s\n</ul>' % u'\n'.join([u'<li>%s</li>'
            % force_unicode(w) for w in self]))

    def my_render(self):
        """My render function

        Kinda dirty, but it works in our case.
        """
        midList = []
        for x, wid in enumerate(self):
            #print(wid)
            if self.actives[x] == False:
                wid.attrs['disabled'] = True
            if self.help_texts[x]:
                help_text = (
                    '<div class="help_tooltip ss_sprite ss_help" '
                    'title="%s">&nbsp;</div>' % self.help_texts[x])
            else:
                help_text = '<div class="help_tooltip">&nbsp;</div>'
            midList.append(
                u'<div class="wizard-item-row">%s%s</div>'
                % (help_text, force_unicode(wid)))
        finalList = mark_safe(
            u'<div class="span9 wizard-radio-select">%s</div>'
            % u'\n'.join(midList))
        return finalList


class ScenarioForm(forms.Form):

    display_title = 'BOWA'

    name = forms.CharField(
        max_length=100,
        required=True,
        label='Hoe wilt u het scenario noemen?',
        help_text='Deze naam wordt gebruikt voor het uitvoerbestand.'
    )

    email = forms.EmailField(
        required=True,
        label='Emailadres',
        help_text='Uw email adres'
    )

    scenario_type = forms.ChoiceField(
        label='Kies het type gebruikersscenario',
        choices=SCENARIO_TYPES,
        widget=forms.widgets.RadioSelect(renderer=CustomRadioSelectRenderer),
    )