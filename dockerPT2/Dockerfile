FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    dnsutils wget gnupg2 build-essential libcurl4-openssl-dev libxml2 libxml2-dev libxslt1-dev ruby ruby-dev cron nmap \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable sslscan hping3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* 

# Install WPScan, wafw00f, playwright
RUN gem install wpscan && \
    pip install --no-cache-dir wafw00f playwright && \
    playwright install chromium --with-deps

# Copy only the requirements.txt first to leverage Docker cache
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Copy and set the entrypoint script
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Setup cron job (every 30 minutes)
COPY cleanup.sh /etc/cron.hourly/cleanup.sh
RUN chmod +x /etc/cron.hourly/cleanup.sh \
    && echo "*/30 * * * * /etc/cron.hourly/cleanup.sh >> /var/log/cron.log 2>&1" | crontab -

EXPOSE 5000

# Start cron and the Flask app
CMD cron && flask run