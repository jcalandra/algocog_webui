from django.forms import ModelForm
from .models import parameter, comment


class parameterForm(ModelForm):
    class Meta:
        model = parameter
        fields = ['file', 'fft', 'cqt', 'mfcc', 'sim_threshold', 'seg_threshold', 'sim_materials', 'diff_concordance',
                  'euclid_distance', 'strict_equality', 'alignment', 'diff_fourier', 'diff_dynamic', 'rule_1', 'rule_2',
                  'rule_3', 'rule_4', 'rule_5', 'transitory_frame']


class commentaryForm(ModelForm):
    class Meta:
        model = comment
        fields = ['music_title', 'comment']

    def id_param(self):
        self.save(commit=False)
        self.parameter = parameter.objects.last()
