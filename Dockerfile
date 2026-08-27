FROM python:3.10-slim

# نصب پیش‌نیازها و کلاینت Cloudflare WARP
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    lsb-release \
    && curl -fsSL https://pkg.cloudflareclient.com/pubkey.gpg | gpg --yes --dearmor --output /usr/share/keyrings/cloudflare-warp-archive-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/cloudflare-warp-archive-keyring.gpg] https://pkg.cloudflareclient.com/cloudflared.deb $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/cloudflare-warp.list \
    && apt-get update && apt-get install -y cloudflare-warp \
    && apt-get clean

WORKDIR /app

# نصب پکیج‌های پایتون
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# اسکریپت استارت‌آپ برای ثبت WARP، تنظیم حالت Proxy و اجرای برنامه
CMD warp-cli --accept-tos registration new && \
    warp-cli --accept-tos mode proxy && \
    warp-cli --accept-tos proxy port 4001 && \
    warp-cli --accept-tos connect && \
    sleep 3 && \
    python main.py
