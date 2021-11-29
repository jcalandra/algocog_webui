from django.urls import path
from . import views

app_name = 'acwebui'
urlpatterns = [
    path('', views.algocog, name='index'),
    path('parametres', views.parameters, name='parameters'),
    path('oops', views.oops, name='oops'),
    path('bdd', views.allresults, name='allresults'),
    path('resultat', views.lastresult, name='result'),
    path('save', views.save, name='save'),
    path('comment', views.save_comment, name='comment'),
    path('parameters_text', views.params_text, name='parameters_text'),

]
