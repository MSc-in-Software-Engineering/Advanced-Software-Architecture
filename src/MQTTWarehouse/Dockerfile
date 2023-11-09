FROM python:3.12-slim
RUN apt-get update 
RUN apt-get install gcc -y
RUN apt-get install python3-dev -y
RUN apt-get install libpq-dev -y
COPY warehouse.py .
COPY requirements.txt .
RUN pip install -r requirements.txt 
CMD ["python", "warehouse.py"]