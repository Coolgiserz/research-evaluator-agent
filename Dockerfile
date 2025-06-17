# Dockerfile for Research Evaluator Agent
FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/python:3.12-slim

WORKDIR /app

# Copy dependency definitions
COPY pyproject.toml uv.lock ./
#ENV UV_PYPI_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
ENV UV_PYPI_INDEX_URL=https://mirrors.aliyun.com/pypi/simple
ENV UV_HTTP_TIMEOUT=300
# Upgrade pip and install uv dependency manager
RUN pip install -i https://mirrors.aliyun.com/pypi/simple --upgrade pip \

    && pip install -i https://mirrors.aliyun.com/pypi/simple uv && uv sync

# Copy project source
COPY . .
RUN chmod +x ./entrypoint.sh
# Expose HTTP API port
EXPOSE 8000

# Default command to start the server
CMD ["./entrypoint.sh"]