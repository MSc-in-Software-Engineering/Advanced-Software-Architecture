FROM python:3.8-slim
COPY warehouse.py .
COPY requirements.txt .
RUN pip install -r requirements.txt 
CMD ["python", "warehouse.py"]