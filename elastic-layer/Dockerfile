FROM python:3.12-slim

WORKDIR /elastic-layer

# get linux dependencies
RUN apt-get update
RUN apt-get -y install libpq-dev gcc

COPY requirements.txt .

# Create a virtual environment and install dependencies
RUN python3 -m venv /elastic-layer/env && \
    /elastic-layer/env/bin/pip install --upgrade pip && \
    /elastic-layer/env/bin/pip install -r requirements.txt

# Ensure the virtual environment binaries are in the PATH
ENV PATH="/elastic-layer/env/bin:$PATH"

ENV DATA_LAYER_URL="localhost:4500"

COPY . .

EXPOSE 4000

CMD ["python3", "wsgi.py"]