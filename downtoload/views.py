from django.shortcuts import get_object_or_404, redirect, render
from .tasks import download_video_task
from .utils.video_downloader import progress_data
from django.http import HttpResponse, FileResponse, JsonResponse
from .forms import VideoDownloadForm
from .utils.video_downloader import download_video
import os
import uuid

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
    message = ""
    video_info = []

    if request.method == "POST":
        form = VideoDownloadForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            action = request.POST.get("action")

            if action == "download":
                task_id = str(uuid.uuid4())
                try:
                    task = download_video_task(url, task_id=task_id)
                    message = f"Video download queued. Task ID: {task.id}"
                except Exception as e:
                    message = f"Error: {str(e)}"

            elif action == "view_info":
                try:
                    # Extract info immediately
                    video_info = download_video(url, extract_flat=True)

                    # Make sure each entry has title and url
                    # video_info = []
                    # for entry in info_list:
                    #     video_info.append({
                    #         "title": entry.get("title", "No title"),
                    #         "url": entry.get("url") or entry.get("webpage_url") or "#"
                    #     })

                except Exception as e:
                    message = f"Error fetching info: {str(e)}"
    else:
        form = VideoDownloadForm()

    return render(
        request,
        "downtoload/download.html",
        {"form": form, "message": message, "video_info": video_info}
    )


def download_progress(request, video_id):
    """
    Returns Json with progress information for a video download.
    """
    data = progress_data.get(video_id, {"status": "not_found"})
    return JsonResponse(data)