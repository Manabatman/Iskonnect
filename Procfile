release: alembic upgrade head
web: gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w ${WEB_CONCURRENCY:-2} -b 0.0.0.0:$PORT --forwarded-allow-ips='*' --proxy-headers
