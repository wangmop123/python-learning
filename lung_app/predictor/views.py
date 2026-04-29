from django.shortcuts import render
from .forms import LungCancerForm
from .ml_service import predict_lung_cancer

def home(request):
    result = None
    error = None

    if request.method == "POST":
        form = LungCancerForm(request.POST)
        if form.is_valid():
            try:
                result = predict_lung_cancer(form.cleaned_feature_dict())
            except Exception as exc:
                error = str(exc)
        else:
            error = "Please correct the form errors."
    else:
        form = LungCancerForm()

    return render(
        request,
        "predictor/index.html",
        {
            "form": form,
            "result": result,
            "error": error,
        },
    )
