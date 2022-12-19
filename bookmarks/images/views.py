from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm


@login_required
def image_create(request):
    form = ImageCreateForm(data=request.POST or request.GET)
    if form.is_valid():
        new_item = form.save(commit=False)
        new_item.user = request.user
        new_item.save()
        messages.success(request, "Image added successfully")
        return redirect(new_item.get_absolute_url())

    return render(
        request,
        "images/image/create.html",
        {"section": "images", "form": form},
    )
