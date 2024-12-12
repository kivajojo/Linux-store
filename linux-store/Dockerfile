FROM python:3.9-slim

WORKDIR /app

RUN echo "deb https://mirrors.aliyun.com/debian/ bullseye main non-free contrib" > /etc/apt/sources.list \
    && echo "deb https://mirrors.aliyun.com/debian-security bullseye-security main" >> /etc/apt/sources.list \
    && echo "deb https://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib" >> /etc/apt/sources.list

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Shanghai

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        default-libmysqlclient-dev \
        build-essential \
	default-mysql-client \  
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/


RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ \
    pip -U \
    && pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ \
    && pip config set install.trusted-host mirrors.aliyun.com \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 8000


COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh
CMD ["/wait-for-it.sh", "db", "python3.9", "manage.py", "runserver", "0.0.0.0:8000"]
