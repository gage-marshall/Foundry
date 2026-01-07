# Foundry Engine - Production Deployment Guide

Complete guide for deploying Foundry Engine to production with Gunicorn.

## Architecture

Foundry uses a production-ready stack:

```
Internet → Load Balancer/Proxy → Gunicorn (Master) → Uvicorn Workers → FastAPI App
```

- **Gunicorn**: Process manager with multiple workers
- **Uvicorn Workers**: ASGI servers handling async requests
- **FastAPI**: Your application

## Why Gunicorn + Uvicorn?

### Reliability
- **Process Monitoring**: Gunicorn automatically restarts failed workers
- **Graceful Restarts**: Workers restart without dropping connections
- **Zero Downtime**: Rolling deploys with multiple workers

### Performance
- **Multiple Workers**: Handle concurrent requests across CPU cores
- **Async Support**: Uvicorn workers handle async FastAPI code
- **Preloading**: Share memory between workers for efficiency

### Production Features
- **Resource Limits**: Max requests per worker prevents memory leaks
- **Timeouts**: Configurable request and graceful shutdown timeouts
- **Health Checks**: Monitor worker health and restart as needed

## Deployment Options

### Option 1: Render (Recommended)

**Pros:**
- Zero configuration (uses `render.yaml`)
- Automatic SSL certificates
- Auto-scaling available
- Git-based deploys
- Free tier available

**Setup:**
1. Push code to GitHub/GitLab
2. Connect repository on Render
3. Set environment variables
4. Deploy automatically

**Configuration:**
```yaml
# render.yaml (already configured)
startCommand: gunicorn main:app -c gunicorn.conf.py
```

### Option 2: AWS/GCP/Azure

**Deploy on VM:**

```bash
# 1. Clone repository
git clone <your-repo>
cd foundry

# 2. Install dependencies
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Set environment variables
export SECRET_KEY="your-secret-key"
export FOUNDRY_ENV="production"
export BREVO_API_KEY="your-api-key"

# 4. Start with systemd
sudo cp foundry.service /etc/systemd/system/
sudo systemctl enable foundry
sudo systemctl start foundry
```

**Systemd Service File:**
```ini
# /etc/systemd/system/foundry.service
[Unit]
Description=Foundry Engine
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/foundry
Environment="PATH=/var/www/foundry/.venv/bin"
EnvironmentFile=/var/www/foundry/.env
ExecStart=/var/www/foundry/.venv/bin/gunicorn main:app -c gunicorn.conf.py
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=30
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

### Option 3: Docker

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 foundry && chown -R foundry:foundry /app
USER foundry

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["gunicorn", "main:app", "-c", "gunicorn.conf.py"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  foundry:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./sites:/app/sites:ro
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Option 4: Kubernetes

**Deployment:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: foundry-engine
spec:
  replicas: 3
  selector:
    matchLabels:
      app: foundry
  template:
    metadata:
      labels:
        app: foundry
    spec:
      containers:
      - name: foundry
        image: your-registry/foundry:latest
        ports:
        - containerPort: 8000
        env:
        - name: FOUNDRY_ENV
          value: "production"
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: foundry-secrets
              key: secret-key
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

## Configuration Tuning

### Worker Count

**Auto-calculated formula:**
```python
workers = (2 to 4) × CPU_cores
```

**Override:**
```bash
export GUNICORN_WORKERS=4
```

**Guidelines:**
- **Low Traffic**: 2-4 workers
- **Medium Traffic**: 4-8 workers
- **High Traffic**: 8+ workers (scale horizontally instead)

### Timeouts

**Request Timeout** (default: 30s):
```python
# gunicorn.conf.py
timeout = 30  # Increase for slow endpoints
```

**Graceful Timeout** (default: 30s):
```python
graceful_timeout = 30  # Time for workers to finish requests
```

### Memory Management

**Max Requests** (default: 1000):
```python
max_requests = 1000  # Restart worker after N requests
max_requests_jitter = 100  # Add randomness
```

This prevents memory leaks by restarting workers periodically.

### Connection Limits

**Worker Connections** (default: 1000):
```python
worker_connections = 1000  # Max simultaneous clients per worker
```

## Monitoring

### Health Checks

**Endpoint:**
```
GET /health
Response: {"status": "healthy", "service": "foundry-engine"}
```

**Use in:**
- Load balancers
- Container orchestrators
- Monitoring tools

### Logging

**Structured Logging:**
```python
# Gunicorn access logs include:
# - IP address
# - Request method and path
# - Status code
# - Response time
# - User agent
```

**Log Levels:**
```bash
export LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### Metrics

**Process Metrics:**
- Worker count
- Worker restarts
- Request rate
- Error rate
- Response times

**Monitor with:**
- Prometheus + Grafana
- DataDog
- New Relic
- Render metrics (built-in)

## Scaling

### Vertical Scaling

Increase server resources:
- More CPU cores → More workers
- More RAM → Handle more connections

### Horizontal Scaling

Multiple instances behind load balancer:
- Better reliability (no single point of failure)
- Better performance (distribute load)
- Zero-downtime deploys (rolling updates)

**Example (Render):**
```yaml
# render.yaml
services:
  - type: web
    numInstances: 3  # Multiple instances
    plan: standard   # More resources per instance
```

## Troubleshooting

### Workers Dying

**Symptoms:** Frequent worker restarts

**Solutions:**
1. Increase timeout if requests are slow
2. Check for memory leaks
3. Review application logs
4. Reduce max_requests if needed

### High Memory Usage

**Solutions:**
1. Reduce worker count
2. Decrease max_requests
3. Enable worker recycling
4. Profile application for leaks

### Slow Response Times

**Solutions:**
1. Increase worker count
2. Add caching
3. Optimize database queries
4. Use async properly

### Connection Refused

**Check:**
1. Gunicorn is running: `ps aux | grep gunicorn`
2. Port is correct: `$PORT` environment variable
3. Firewall allows traffic
4. Health check passes

## Security Checklist

- [ ] `SECRET_KEY` is set and secure (32+ chars)
- [ ] `FOUNDRY_ENV=production`
- [ ] HTTPS enabled (Render does this automatically)
- [ ] Security headers enabled (automatic)
- [ ] Rate limiting enabled
- [ ] Allowed hosts configured
- [ ] Email credentials secured
- [ ] No secrets in repository
- [ ] Regular dependency updates

## Performance Checklist

- [ ] Gunicorn with multiple workers
- [ ] Worker count optimized for traffic
- [ ] Preload app enabled
- [ ] Max requests configured
- [ ] Static files served efficiently
- [ ] Caching headers set
- [ ] Database connection pooling (if needed)
- [ ] Async/await used properly

## Backup and Recovery

### What to Backup

1. **Site Content**: `sites/` directory
2. **Environment Config**: `.env` file (securely!)
3. **Custom Code**: Any modifications to engine

### Backup Strategy

```bash
# Create backup
tar -czf foundry-backup-$(date +%Y%m%d).tar.gz \
    sites/ \
    .env \
    gunicorn.conf.py

# Upload to S3/GCS/Azure
aws s3 cp foundry-backup-*.tar.gz s3://your-backup-bucket/
```

### Recovery

```bash
# Restore backup
tar -xzf foundry-backup-20250107.tar.gz

# Restart service
sudo systemctl restart foundry
```

## Zero-Downtime Deploys

### Strategy

1. **Rolling Restart**: Gunicorn restarts workers one at a time
2. **Blue-Green**: Deploy to new instances, switch traffic
3. **Canary**: Route small % of traffic to new version

### Gunicorn Reload

```bash
# Graceful reload (zero downtime)
kill -HUP $GUNICORN_PID

# Or with systemd
sudo systemctl reload foundry
```

## Support

For deployment issues:
1. Check logs: `journalctl -u foundry -f`
2. Verify config: `gunicorn main:app -c gunicorn.conf.py --check-config`
3. Test locally: `FOUNDRY_ENV=production python main.py`
4. Review documentation
5. Open GitHub issue

---

**Foundry Engine** - Production-ready deployment made simple.
