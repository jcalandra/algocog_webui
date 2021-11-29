"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from . import views, settings

urlpatterns = [
    path('', views.index, name='index'),
    path('index-en/', views.index_en, name='index-en'),
    path('oops/', views.parameters_oops, name='oops'),

    path('these-fr/', views.these_fr, name='these-fr'),
    path('contact-fr/', views.contact_fr, name='contact-fr'),
    path('apropos-fr/', views.apropos_fr, name='apropos-fr'),
    path('formation-fr/', views.formation_fr, name='formation-fr'),
    path('141119-fr/', views.seminaire1_fr, name='141119-fr'),
    path('280521-fr/', views.seminaire2_fr, name='280521-fr'),

    path('thesis-en/', views.thesis_en, name='thesis-en'),
    path('contact-en/', views.contact_en, name='contact-en'),
    path('about-en/', views.about_en, name='about-en'),
    path('formation-en/', views.formation_en, name='formation-en'),
    path('141119-en/', views.seminar1_en, name='141119-en'),
    path('280521-en/', views.seminar2_en, name='280521-en'),

    path('algocognitif-web-interface/', include('acwebui.urls')),
    path('admin/', admin.site.urls),

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
