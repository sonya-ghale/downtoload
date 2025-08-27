from .huey_instance import huey
from .utils.video_downloader import download_video
from django.http import JsonResponse

@huey.task()
def add(a, b):
    print(f"Adding {a} and {b}")
    return a + b

@huey.task()
def sub(a, b):
    print(f"Subtracting {a} and {b}")
    return a - b

@huey.task()
def multiply(a, b):
    print(f"Multiplying {a} and {b}")
    return a * b

@huey.task()
def download_video_task(url):
    """
    Background task to download video via huey
    """
    try:
        file_path = download_video(url)
        print(f"finished downloading: {file_path}")
        return file_path
    except Exception as e:
        return JsonResponse({"error": str(e)})
    # print(f"Starting download for {url}")
    # file_path = download_video(url)
    # print(f"finished downloading: {file_path}")
    # return file_path

"""
@huey.task() decorator tell huey( function is allowed to run in the bc)
it schedules the function to be executed later by consumer
"""