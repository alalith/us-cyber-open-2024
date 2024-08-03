FROM ubuntu:latest

# Install packages
RUN apt-get update && apt-get install -y python3 python3-pip

# Upgrade pip
RUN python3 -m pip install --upgrade pip

# Install dependencies
RUN pip3 install gunicorn Flask tensorflow pillow

# Copy flag
COPY flag.txt /flag.txt

# Protect flag
RUN chmod 444 /flag.txt

# add user
RUN groupadd www && useradd -rm -d /app -s /usr/sbin/nologin -g www -u 1000 www

# Switch working environment
WORKDIR /app

# Add application
COPY challenge .

RUN chmod -R 755 /app
RUN mkdir /app/uploads && chmod 777 /app/uploads

# Expose port the server is reachable on
EXPOSE 1337

# Disable pycache
ENV PYTHONDONTWRITEBYTECODE=1

USER www

# Run supervisord
CMD ["gunicorn","--workers","5","--threads","8","--preload","--timeout","0","run:app","-b",":1337"]