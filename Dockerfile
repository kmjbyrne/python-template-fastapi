FROM python:3.12.6

WORKDIR /usr/src/app

RUN echo "Rust installed at $(date)"
RUN apt-get update && \
    apt-get install -y curl build-essential && \
    rm -rf /var/lib/apt/lists/*
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:$PATH"

COPY requirements.txt .
RUN pip install pip --upgrade
RUN pip install pipenv --no-cache-dir
RUN pip install -r requirements.txt

# finalize layer
COPY . .

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["python", "main.py"]
