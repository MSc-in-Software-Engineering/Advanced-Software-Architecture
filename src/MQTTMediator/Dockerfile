FROM python:3.8-slim
COPY mqtt_mediator.py .
COPY requirements.txt .
RUN pip install -r requirements.txt 
CMD ["python", "mqtt_mediator.py"]