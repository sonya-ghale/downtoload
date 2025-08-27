from huey import RedisHuey

# Redis running locally on default port 6379
huey = RedisHuey('video-downloader', host='127.0.0.1', port=9379)