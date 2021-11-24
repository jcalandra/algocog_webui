from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import parameterForm, commentaryForm
from .models import parameter
from .models import formalDiagram
from .src.oracle_version.main_mso import mso_exec
from django.http import HttpResponse



#comment
# Create your views here.

# Generate Textfile parameters
def params_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=parameters.txt'
    lines = []
    element = parameter.objects.last()
    lines.append("File : " + str(element.file) + "\n")
    lines.append("Similarity Threshold : " + str(element.sim_threshold) + "\n")
    lines.append("Segmentation Threshold : " + str(element.seg_threshold) + "\n")
    lines.append("Color similarity materials Threshold : " + str(element.sim_materials) + "\n")
    lines.append("FFT : " + str(element.fft) + "\n")
    lines.append("CQT : " + str(element.cqt) + "\n")
    lines.append("MFCC : " + str(element.mfcc) + "\n")
    lines.append("Differential Concordance : " + str(element.diff_concordance) + "\n")
    lines.append("Euclidian Distance : " + str(element.euclid_distance) + "\n")
    lines.append("Strict Equality : " + str(element.strict_equality) + "\n")
    lines.append("Alignment : " + str(element.alignment) + "\n")
    lines.append("Differancial Fourier Transform : " + str(element.diff_fourier) + "\n")
    lines.append("Differancial Dynamic : " + str(element.diff_dynamic) + "\n")
    lines.append("Rule 1 (similarity) : " + str(element.rule_1) + "\n")
    lines.append("Rule 2 (validated hypothesis) : " + str(element.rule_2) + "\n")
    lines.append("Rule 3 (existing object) : " + str(element.rule_3) + "\n")
    lines.append("Rule 4 (recomputed object) : " + str(element.rule_4) + "\n")
    lines.append("Rule 5 (regathering) : " + str(element.rule_5) + "\n")
    lines.append("Display Transitory Frames : " + str(element.transitory_frame) + "\n")
    response.writelines(lines)
    return response


def algocog(request):
    return render(request, 'acwebui/index.html')


def parameters(request):
    if request.method == "POST":
        form = parameterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/algocognitif-web-interface/save')
    else:
        form = parameterForm()
    return render(request, 'acwebui/parameters.html', {'form': form})


def oops(request):
    return render(request, 'acwebui/parameters_oops.html')


def allresults(request):
    if request.method == "POST":
        form = commentaryForm(request.POST).save()
        return redirect('/algocognitif-web-interface/comment')
    else:
        form = commentaryForm()
    return render(request, 'acwebui/all_results.html', {'dataParameter':parameter.objects.all(), 'form': form})


def lastresult(request):
    if request.method == "POST":
        form = commentaryForm(request.POST).save()
        print("comment form is ok")
        return redirect('/algocognitif-web-interface/comment')
    else:
        mso_exec()
        form = commentaryForm()
        print("comment form does not work")
    return render(request, 'acwebui/last_result.html', {'element': parameter.objects.last(),
                                                        'formaldiagram': formalDiagram.objects.last(),
                                                        'form': form})


def save(request):
    return render(request, 'acwebui/save.html', {'element': parameter.objects.last()})


def save_comment(request):
    return render(request, 'acwebui/save_comment.html')