FROM python:3

# Install packages
RUN apt-get update && apt-get install -y supervisor

# Upgrade pip
RUN python -m pip install --upgrade pip

# Install dependencies
RUN pip install gunicorn Flask pycryptodome

RUN useradd -rm -d /app -s /usr/sbin/nologin www

# add user
#RUN adduser -D -u 1000 -g 1000 -s /usr/sbin/nologin www

# Switch working environment
WORKDIR /app

# Add application
COPY challenge .

# Add firmware
COPY firmware.bin /firmware.bin

RUN chmod -R 755 /app && chmod 777 /app/assets/firmware_updates && chmod 777 /app/instance

# Setup supervisor
COPY config/supervisord.conf /etc/supervisord.conf

# Expose port the server is reachable on
EXPOSE 80

# Disable pycache
ENV PYTHONDONTWRITEBYTECODE=1

# Run supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]