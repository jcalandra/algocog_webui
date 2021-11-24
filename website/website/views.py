from django.shortcuts import render

# pages principales
def index(request):
    return render(request, 'index.html')

def index_en(request):
    return render(request, 'index-en.html')

def parameters_oops(request):
    return render(request, 'parameters_oops.html')

# pages en français
def these_fr(request):
    return render(request, 'fr/these-fr.html')

def contact_fr(request):
    return render(request, 'fr/contact-fr.html')

def apropos_fr(request):
    return render(request, 'fr/apropos-fr.html')

def formation_fr(request):
    return render(request, 'fr/formation-fr.html')

def seminaire1_fr(request):
    return render(request, 'fr/141119-fr.html')

def seminaire2_fr(request):
    return render(request, 'fr/280521-fr.html')

# pages en anglais
def thesis_en(request):
    return render(request, 'en/thesis-en.html')

def contact_en(request):
    return render(request, 'en/contact-en.html')

def about_en(request):
    return render(request, 'en/about-en.html')

def formation_en(request):
    return render(request, 'en/formation-en.html')

def seminar1_en(request):
    return render(request, 'en/141119-en.html')

def seminar2_en(request):
    return render(request, 'en/280521-en.html')
