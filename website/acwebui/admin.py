from django.contrib import admin

from .models import parameter, parameterAdmin, comment
from .models import formalDiagram

# Register your models here.
admin.site.register(parameter, parameterAdmin)
admin.site.register(formalDiagram)
admin.site.register(comment)
