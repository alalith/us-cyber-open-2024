FROM python:3-alpine

# Upgrade pip
RUN python -m pip install --upgrade pip

# Install dependencies
RUN pip install flask gunicorn redis

# add user
RUN adduser -D -u 1000 -g 1000 -s /usr/sbin/nologin www

# Switch working environment
WORKDIR /app

# Add application
COPY challenge .

# Expose port the server is reachable on
EXPOSE 80

# Disable pycache
ENV PYTHONDONTWRITEBYTECODE=1

# Run supervisord
CMD ["gunicorn","--workers","5","--threads","8","--preload","--timeout","0","run:app","-b",":80"]