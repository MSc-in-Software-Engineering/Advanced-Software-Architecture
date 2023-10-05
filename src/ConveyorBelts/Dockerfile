FROM python:3.8-slim
COPY conveyor_belt_component.py ./conveyor_belt_component.py
RUN pip install paho-mqtt
CMD ["python", "conveyor_belt_component.py"]
