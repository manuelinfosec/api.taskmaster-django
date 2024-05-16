"""Gunicorn production configuration"""
import multiprocessing

# bind
bind = "0.0.0.0:8000"

workers = multiprocessing.cpu_count() * 2 + 1
# reload_engine = "inotify"
group = "user"
user = "user"
reload = True

# logs
loglevel = "debug"
accesslog = "/tmp/gunicorn.access"
errorlog = "/tmp/gunicorn.error"
