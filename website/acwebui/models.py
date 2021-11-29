from django.db import models
from django.contrib import admin
import os


# Create your models here.
class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class parameter(TimestampModel):
    file = models.FileField(upload_to='audio')
    fft = models.BooleanField(default=False)
    cqt = models.BooleanField(default=True)
    mfcc = models.BooleanField(default=False)
    sim_threshold = models.FloatField(default=0.975)
    seg_threshold = models.FloatField(default=150)
    sim_materials = models.FloatField(default=0.94)
    # similarity rules
    diff_concordance = models.BooleanField(default=True)
    euclid_distance = models.BooleanField(default=False)
    strict_equality = models.BooleanField(default=False)
    alignment = models.BooleanField(default=True)
    # segmentation rules
    diff_fourier = models.BooleanField(default=True)
    diff_dynamic = models.BooleanField(default=False)
    rule_1 = models.BooleanField(default=True)
    rule_2 = models.BooleanField(default=True)
    rule_3 = models.BooleanField(default=True)
    rule_4 = models.BooleanField(default=True)
    rule_5 = models.BooleanField(default=True)

    transitory_frame = models.BooleanField(default=False)


class formalDiagram(TimestampModel):
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=400)
    parameter = models.ForeignKey(parameter, on_delete=models.CASCADE)

    def split(self):
        name, format = os.path.splitext(self.image.name.split('/')[-1])
        return name + format


class comment(TimestampModel):
    name = models.CharField(default='Jean', max_length=50)
    surname = models.CharField(default='Dupont', max_length=50)
    email = models.EmailField(default='jean.dupont@mail.fr', max_length=254)
    musicologist = models.BooleanField(default=False)
    musician = models.BooleanField(default=False)
    music_title = models.CharField(default='Music Title', max_length=150)
    comment = models.TextField(default='Laissez un commentaire...')
    parameter = models.OneToOneField(parameter, on_delete=models.CASCADE, default=parameter.objects.last())



class parameterAdmin(admin.ModelAdmin):
    list_display = ('file', 'sim_threshold', 'seg_threshold', 'created_at', 'updated_at')
    list_filter = ('file',)
    search_fields = ['file', 'sim_threshold']

