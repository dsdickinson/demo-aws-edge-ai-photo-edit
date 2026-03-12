FROM nvcr.io/nvidia/pytorch:24.08-py3-igpu

WORKDIR /
COPY app /app

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

CMD ["python3", "/app/main.py"]
