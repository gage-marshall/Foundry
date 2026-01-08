"""Gunicorn configuration for production deployment."""

import multiprocessing
import os

# Determine number of workers
# For CPU-bound: (2 x $num_cores) + 1
# For I/O-bound (our case): (2-4) x $num_cores
workers_per_core = 2
max_workers = 8
min_workers = 2

# Get number of CPU cores
cores = multiprocessing.cpu_count()
default_workers = workers_per_core * cores

# Calculate workers (bounded)
workers = max(min_workers, min(default_workers, max_workers))

# Override with environment variable if set
workers = int(os.getenv("GUNICORN_WORKERS", workers))

# Worker class - use uvicorn workers for ASGI
worker_class = "uvicorn.workers.UvicornWorker"

# Binding
bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"

# Logging
accesslog = "-"  # stdout
errorlog = "-"   # stderr
loglevel = os.getenv("LOG_LEVEL", "info").lower()
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Worker timeout (30 seconds - adjust based on your needs)
timeout = 30
graceful_timeout = 30
keepalive = 5

# Worker lifecycle
max_requests = 1000  # Restart worker after this many requests (prevents memory leaks)
max_requests_jitter = 100  # Add randomness to prevent all workers restarting at once

# Process naming
proc_name = "foundry-engine"

# Preload app for better performance and memory sharing
preload_app = True

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

# Server mechanics
daemon = False  # Don't daemonize (container/Render will manage)
pidfile = None  # No pidfile needed
umask = 0o007
user = None
group = None
tmp_upload_dir = None

# Worker connections (max simultaneous clients per worker)
worker_connections = 1000

# Forwarded headers (important for proxies/load balancers)
forwarded_allow_ips = "*"  # Trust Render's proxy headers


def on_starting(server):
    """Called just before the master process is initialized."""
    server.log.info(f"Foundry Engine starting with {workers} workers")


def on_reload(server):
    """Called when server is reloading."""
    server.log.info("Foundry Engine reloading...")


def when_ready(server):
    """Called just after the server is started."""
    server.log.info(f"Foundry Engine ready on {bind}")


def on_exit(server):
    """Called just before exiting."""
    server.log.info("Foundry Engine shutting down")


def worker_int(worker):
    """Called when worker receives SIGINT or SIGQUIT."""
    worker.log.info(f"Worker {worker.pid} received shutdown signal")


def worker_abort(worker):
    """Called when worker receives SIGABRT."""
    worker.log.warning(f"Worker {worker.pid} aborted")


def pre_fork(server, worker):
    """Called just before a worker is forked."""
    pass


def post_fork(server, worker):
    """Called just after a worker has been forked."""
    server.log.info(f"Worker spawned (pid: {worker.pid})")


def pre_exec(server):
    """Called just before a new master process is forked."""
    server.log.info("Forking new master process")


def pre_request(worker, req):
    """Called just before a worker processes a request."""
    worker.log.debug(f"{req.method} {req.path}")


def post_request(worker, req, environ, resp):
    """Called after a worker processes a request."""
    pass


def child_exit(server, worker):
    """Called just after a worker has been exited."""
    server.log.info(f"Worker exited (pid: {worker.pid})")


def worker_exit(server, worker):
    """Called just after a worker has been exited."""
    pass


def nworkers_changed(server, new_value, old_value):
    """Called just after number of workers has been changed."""
    server.log.info(f"Workers changed from {old_value} to {new_value}")


def on_exit(server):
    """Called just before exiting."""
    server.log.info("Foundry Engine shutting down gracefully")
