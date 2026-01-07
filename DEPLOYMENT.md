# Deployment Guide

## Pre-Deployment Checklist

### Security
- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Set `debug=False` in production
- [ ] Configure all environment variables
- [ ] Remove any hardcoded credentials
- [ ] Enable HTTPS/SSL
- [ ] Set up proper firewall rules

### Database
- [ ] Migrate from SQLite to PostgreSQL (recommended)
- [ ] Set up database backups
- [ ] Configure database connection pooling
- [ ] Test database migrations

### Application
- [ ] Use production WSGI server (Gunicorn/uWSGI)
- [ ] Set up process manager (systemd/supervisor)
- [ ] Configure logging
- [ ] Set up monitoring
- [ ] Configure rate limiting
- [ ] Set up error tracking

## Production Deployment Options

### Option 1: Using Gunicorn (Recommended)

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app:app

# With SSL
gunicorn -w 4 -b 0.0.0.0:443 --certfile cert.pem --keyfile key.pem app:app
```

### Option 2: Using uWSGI

```bash
# Install uWSGI
pip install uwsgi

# Run with uWSGI
uwsgi --http :5000 --module app:app --processes 4
```

### Option 3: Docker (Future)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## Environment Variables

Create `.env` file (never commit this):

```bash
SECRET_KEY=your-strong-random-secret-key-here
LLM_PROVIDER=huggingface
HUGGINGFACE_API_KEY=your-api-key
OLLAMA_URL=http://localhost:11434
DATABASE_URL=postgresql://user:pass@localhost/finance_db
DEBUG=False
```

## PostgreSQL Setup

1. Install PostgreSQL
2. Create database:
   ```sql
   CREATE DATABASE finance_db;
   CREATE USER finance_user WITH PASSWORD 'strong_password';
   GRANT ALL PRIVILEGES ON DATABASE finance_db TO finance_user;
   ```
3. Update `memory/db.py` to use PostgreSQL
4. Run migrations

## Nginx Configuration (Reverse Proxy)

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Systemd Service

Create `/etc/systemd/system/finance-ai.service`:

```ini
[Unit]
Description=Financial Advisor AI
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/financial_agentic_ai
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable finance-ai
sudo systemctl start finance-ai
```

## Monitoring

- Set up application monitoring (Sentry, etc.)
- Monitor database performance
- Set up log aggregation
- Configure alerts

## Backup Strategy

- Daily database backups
- Store backups off-site
- Test backup restoration
- Document recovery procedures

---

**Remember**: Never commit `.env` files or database files to version control!

