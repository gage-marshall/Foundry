"""Gunicorn configuration for production deployment."""

import multiprocessing
import os

# Determine number of workers
workers_per_core = 2
max_workers = 8
min_workers = 2

cores = multiprocessing.cpu_count()
default_workers = workers_per_core * cores
workers = max(min_workers, min(default_workers, max_workers))
workers = int(os.getenv("GUNICORN_WORKERS", workers))

# Worker class - use uvicorn workers for ASGI
worker_class = "uvicorn.workers.UvicornWorker"

# Binding
bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"

# Logging
accesslog = "-"
errorlog = "-"
loglevel = os.getenv("LOG_LEVEL", "info").lower()
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Worker timeout
timeout = 30
graceful_timeout = 30
keepalive = 5

# Worker lifecycle
max_requests = 1000
max_requests_jitter = 100

# Process naming
proc_name = "foundry-engine"

# Preload app
preload_app = True

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

# Server mechanics
daemon = False
pidfile = None
umask = 0o007
user = None
group = None
tmp_upload_dir = None

worker_connections = 1000
forwarded_allow_ips = "*"


def on_starting(server):
    server.log.info(f"Foundry Engine starting with {workers} workers")


def on_reload(server):
    server.log.info("Foundry Engine reloading...")


def when_ready(server):
    server.log.info(f"Foundry Engine ready on {bind}")


def on_exit(server):
    server.log.info("Foundry Engine shutting down gracefully")


def worker_int(worker):
    worker.log.info(f"Worker {worker.pid} received shutdown signal")


def worker_abort(worker):
    worker.log.warning(f"Worker {worker.pid} aborted")


def post_fork(server, worker):
    server.log.info(f"Worker spawned (pid: {worker.pid})")


def pre_exec(server):
    server.log.info("Forking new master process")


def pre_request(worker, req):
    worker.log.debug(f"{req.method} {req.path}")


def child_exit(server, worker):
    server.log.info(f"Worker exited (pid: {worker.pid})")


def nworkers_changed(server, new_value, old_value):
    server.log.info(f"Workers changed from {old_value} to {new_value}")
