# Indie AI: A gradio APP to run multiple AI apps
Build the container (name: indieai):

```
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    apt-utils \
    build-essential \
    gcc \
    g++ \
    curl \
    software-properties-common \
    git \
    ffmpeg\
    && rm -rf /var/lib/apt/lists/*\
    && /usr/local/bin/python -m pip install --upgrade pip

RUN git clone https://github.com/procrastinando/indieai.git .

RUN if [ -x "$(command -v nvidia-smi)" ]; then \
        pip3 install torch torchvision torchaudio; \
    else \
        pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu; \
    fi

RUN pip3 install -r requirements.txt

EXPOSE 85

ENTRYPOINT ["python3", "app.py"]
```
Save the `Dockerfile` and build it: `docker build -t indieai .`, then deploy this in docker compose:
```
version: '3'
services:
  app:
    image: indieai
    ports:
      - "85:85"
    restart: unless-stopped
```
