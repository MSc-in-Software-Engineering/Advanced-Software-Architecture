FROM python:3.8-slim
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY robotic_arm.py .
CMD ["python", "robotic_arm.py"]