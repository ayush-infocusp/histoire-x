# syntax=docker/dockerfile:1
FROM python:3.9-slim-buster AS build

WORKDIR /python-docker
COPY requirements.txt ./
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libsndfile1 && \
    rm -rf /var/lib/apt/lists/*
COPY . .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html

# Final cleanup to reduce image size
RUN apt-get purge -y build-essential && \
    apt-get autoremove -y && \
    rm -rf /root/.cache/pip

EXPOSE 5002

# CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
CMD ["gunicorn", "--bind", "0.0.0.0:5002", "app:app"]




# # syntax=docker/dockerfile:1
# FROM python:3.9-slim AS build

# WORKDIR /python-docker
# COPY requirements.txt ./
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential libsndfile1 && \
#     rm -rf /var/lib/apt/lists/*
# COPY . .
# RUN pip install --no-cache-dir --upgrade pip && \
#     pip install --no-cache-dir -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html

# # Final cleanup to reduce image size
# RUN apt-get purge -y build-essential && \
#     apt-get autoremove -y && \
#     rm -rf /root/.cache/pip

# EXPOSE 5001

# CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
