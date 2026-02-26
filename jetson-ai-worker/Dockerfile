FROM nvcr.io/nvidia/l4t-pytorch:r35.3.1

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python3", "app/main.py"]
