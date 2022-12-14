from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from django.shortcuts import get_object_or_404
from .models import Image
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required, is_ajax
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from actions.utils import create_action
from django.conf import settings
import redis


redis_client = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


@login_required
def image_create(request):
    form = ImageCreateForm(data=request.POST or request.GET)
    if form.is_valid():
        new_item = form.save(commit=False)
        new_item.user = request.user
        new_item.save()
        create_action(request.user, "bookmarked image", new_item)
        messages.success(request, "Image added successfully")
        return redirect(new_item.get_absolute_url())

    return render(
        request,
        "images/image/create.html",
        {"section": "images", "form": form},
    )


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    total_views = redis_client.incr(f"image:{image.id}:views")
    redis_client.zincrby("image_ranking", 1, image.id)
    return render(
        request,
        "images/image/detail.html",
        {"section": "images", "image": image, "total_views": total_views},
    )


@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get("id")
    action = request.POST.get("action")
    try:
        image = Image.objects.get(id=image_id)
        if action == "like":
            image.users_like.add(request.user)
            create_action(request.user, "likes", image)
            return JsonResponse({"status": "ok"})
        elif action == "unlike":
            image.users_like.remove(request.user)
            return JsonResponse({"status": "ok"})
    except Exception:
        pass
    return JsonResponse({"status": "error"})


class ImageListView(ListView):
    model = Image
    paginate_by = 6
    context_object_name = "images"

    def get_template_names(self):
        return (
            "images/image/list_ajax.html"
            if is_ajax(self.request)
            else "images/image/list.html"
        )
