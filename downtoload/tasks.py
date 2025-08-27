from .huey_instance import huey
from .utils.video_downloader import download_video, progress_data
from django.http import JsonResponse
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

from django.conf import settings
from huey import crontab

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
def download_video_task(url, task_id):
    from .utils.video_downloader import progress_data
    try:
        progress_data[task_id] = {"status": "downloading"}
        print(f"[Task {task_id}] Download started...")
        file_path = download_video(url)
        progress_data[task_id] = {"status": "finished", "file": file_path}
        print(f"[Task {task_id}] Download finished: {file_path}")
        return file_path
    except Exception as e:
        progress_data[task_id] = {"status": "error", "error": str(e)}
        print(f"[Task {task_id}] Error: {e}")
        return None


"""
@huey.task() decorator tell huey( function is allowed to run in the bc)
it schedules the function to be executed later by consumer
"""