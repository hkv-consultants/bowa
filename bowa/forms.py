from django import forms
import gdal
import logging
import os
import shutil
import tempfile
from bowa.models import BowaScenario
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from bowa.util import gdal_open

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

    lg = forms.FileField(
        label="Landgebruik",
        required=True,
        help_text="Landgebruik en open water")

    fouten = forms.FileField(
        label="Foutenmatrix landgebruik",
        required=True,
        help_text="Foutenmatrix behorende bij de landgebruik kaart")

    normen = forms.FileField(
        label="Normen",
        required=True,
        help_text="Bestand waarin de normen worden beschreven.")

    ah = forms.FileField(
        label="Maaiveldhoogten",
        required=True,
        help_text="Rasterbestand met maaiveldhoogten")

    te = forms.FileField(
        label="Toetseenheden",
        required=True,
        help_text="Rasterbestand met toetseenheden")

    pg = forms.FileField(
        label="Peilgebieden",
        required=True,
        help_text="Rasterbestand met peilgebieden")

    ht10 = forms.FileField(
        label="Waterstanden HT10",
        required=True,
        help_text="Maatgevende waterstanden met een herhalingstijd van 10 jaar")

    ht25 = forms.FileField(
        label="Waterstanden HT25",
        required=True,
        help_text="Maatgevende waterstanden met een herhalingstijd van 25 jaar")

    ht50 = forms.FileField(
        label="Waterstanden HT50",
        required=True,
        help_text="Maatgevende waterstanden met een herhalingstijd van 50 jaar")

    ht100 = forms.FileField(
        label="Waterstanden HT100",
        required=True,
        help_text="Maatgevende waterstanden met een herhalingstijd van 100 jaar")

    ahdev = forms.FloatField(
        label="Onzekerheidsmarge maaiveldhoogte [m]",
        required=True,
        help_text="Niet negatieve waarde voor de afwijking in de maaiveldhoogte")

    htdev = forms.FloatField(
        label="Onzekerheidsmarge waterhoogte [m]",
        required=True,
        help_text="Niet negatieve waarde voor de afwijking in de waterhoogte")

    scenario_type = forms.ChoiceField(
        label='Kies het type scenario',
        choices=SCENARIO_TYPES,
        widget=forms.widgets.RadioSelect(renderer=CustomRadioSelectRenderer),
        help_text="Scenario type")

    nsim = forms.IntegerField(
        label="Aantal simulaties",
        required=True,
        help_text="Hoeveel Monte Carlo simulatioes moeten er worden gemaakt")


    @property
    def temp_directory(self):
        if not hasattr(self, '_temp_directory'):
            self._temp_directory = tempfile.mkdtemp()
        return self._temp_directory

    def add_field_error(self, field, message):
        """Assumes this field has no errors yet"""
        self._errors[field] = self.error_class([message])

    def save_to_temp_directory(self, fieldname):
        uploadedfile = self.cleaned_data.get(fieldname)
        if uploadedfile is None:
            return

        filename = os.path.join(self.temp_directory, uploadedfile.name)
        with open(filename, 'wb') as f:
            for chunk in uploadedfile.chunks():
                f.write(chunk)
        return filename

    def save_file(self, fieldname):
        path = self.save_to_temp_directory(fieldname)

        if not hasattr(self, 'metadata'):
            self.metadata = {}
        self.metadata[fieldname] = {
            'path': path
            }

        return self.cleaned_data.get(fieldname)

    def save_raster(self, fieldname):
        self.save_file(fieldname)
        path = self.metadata[fieldname]['path']

        dataset = gdal_open(path)

        if dataset is None:
            self.add_field_error(fieldname, 'Kan rasterbestand niet openen')
            return self.cleaned_data.get(fieldname)

        shape = dataset.GetRasterBand(1).ReadAsArray().shape

        self.metadata[fieldname] = {
            'path': path,
            'shape': shape,
            'geotransform': dataset.GetGeoTransform()
            }

        return self.cleaned_data.get(fieldname)

    def clean_lg(self):
        return self.save_raster('lg')

    def clean_normen(self):
        return self.save_file('normen')

    def clean_fouten(self):
        return self.save_file('fouten')

    def clean_ah(self):
        return self.save_raster('ah')

    def clean_te(self):
        return self.save_raster('te')

    def clean_pg(self):
        return self.save_raster('pg')

    def clean_ht10(self):
        return self.save_raster('ht10')

    def clean_ht25(self):
        return self.save_raster('ht25')

    def clean_ht50(self):
        return self.save_raster('ht50')

    def clean_ht100(self):
        return self.save_raster('ht100')

    def clean(self):
        cleaned_data = super(ScenarioForm, self).clean()

        if not hasattr(self, 'metadata'):
            return

        lg_shape = self.metadata['lg']['shape']
        lg_geotransform = self.metadata['lg']['geotransform']

        for fieldname in self.metadata:
            if fieldname == 'lg':
                continue  # No need to compare with itself
            data = self.metadata[fieldname]
            if 'shape' not in data:
                # Not a raster
                continue

            if (data['shape'] != lg_shape or
                data['geotransform'] != lg_geotransform):
                self.add_field_error(
                    fieldname,
                    "Raster heeft niet dezelfde extent of resolutie als het grondgebruikbestand")

        return cleaned_data

    def remove_tempdir(self):
        shutil.rmtree(self.temp_directory)

