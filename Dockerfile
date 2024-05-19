FROM python:3-slim
WORKDIR /programas/api-images
RUN pip3 install flask flask-cors mysql-connector-python

COPY . .
CMD ["python3", "main.py"]
