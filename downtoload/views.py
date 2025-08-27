from django.shortcuts import get_object_or_404, redirect, render
from .tasks import download_video_task
from .utils.video_downloader import progress_data
from django.http import HttpResponse, FileResponse, JsonResponse
from .forms import VideoDownloadForm
import os

def home(request):
    # render's a template with contect
    # redirect("downtoload/home/")
    return render(request, "downtoload/home.html")

# ==== only do this if each button needs a very different response
def hello(request):
    # returning raw response can control what's inside html, json, plain text
    return HttpResponse(f"<p>Hello from here Hello request </p>")

def message(request):
    data ={"message": "Hello", "status": "success"}
    return JsonResponse(data)
    # return JsonResponse({"html": f'<p>{data["message"]} ({data["status"]})</p>'})
#==================================

def action_handler(request):
    action = request.GET.get("action")

    if action == "hello":
        return HttpResponse("Hello from action handler")
    elif action == "message":
        return JsonResponse({"message": "yo", "status": "Success"})
    else:
        return HttpResponse("Unknow action")




def download_view(request):
    if request.method == "POST":
        form = VideoDownloadForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            try:
                # Queue the task in Huey
                task = download_video_task(url)  # returns AsyncResult
                return JsonResponse({
                    "task_id": task.id,
                    "status": "queued",
                    "message": "Your video is being downloaded."
                })
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
    else:
        form = VideoDownloadForm()

    return render(request, "downtoload/download.html", {"form": form})


# def download_progress(request, video_id):
#     """
#     Returns Json with progress information for a video download.
#     """
#     data = progress_data.get(video_id, {"status": "not_found"})
#     return JsonResponse(data)